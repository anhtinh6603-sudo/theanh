"""Bot 5 - Video Render

Turns a finished draft (title + body + 1 image from Bot 4) into a vertical
Shorts video: the LLM breaks the article into a short scene-by-scene script,
each scene gets a TTS narration track, and ffmpeg renders each scene as a
Ken Burns pan/zoom on the article's image with a burned-in caption, then
concatenates everything into one final MP4.

Requires a system `ffmpeg` build with libx264, libfreetype and libfontconfig
(the default for `apt install ffmpeg` / `brew install ffmpeg`).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
import shutil
import subprocess
import tempfile
import textwrap

import config
import llm
from utils import iter_drafts, write_draft

log = logging.getLogger("bot5_video_render")

FPS = 30
MAX_SCENES = 8
CAPTION_FONTSIZE = 56
CAPTION_WRAP_WIDTH = 22  # chars/line, tuned for CAPTION_FONTSIZE on a 1080px-wide frame

SCRIPT_SYSTEM_PROMPT = """Bạn là biên kịch video ngắn (Shorts/Reels). Dựa vào bài viết được \
cung cấp, hãy chia thành 4-8 cảnh (scene) để dựng thành 1 video dọc 45-60 giây. Mỗi cảnh gồm \
lời thoại (narration) ngắn gọn, tự nhiên khi đọc thành tiếng, và caption hiển thị trên màn hình \
(rút gọn từ narration, tối đa khoảng 12 từ để vừa 1 màn hình dọc). Trả lời CHỈ bằng JSON hợp lệ \
theo schema:
{
  "scenes": [
    {"narration": "câu thoại sẽ được chuyển thành giọng đọc", "caption": "chữ hiển thị trên video"}
  ]
}"""


def _script_prompt(title: str, body: str) -> str:
    return f"Tiêu đề: {title}\n\nNội dung bài viết:\n{body[:3000]}"


def _escape_filter_path(path: str) -> str:
    """Escape a path used as a drawtext option value (wrapped in single quotes)."""
    return path.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")


async def _tts_edge(text: str, out_path: Path) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, config.TTS_VOICE)
    await communicate.save(str(out_path))


def _tts_openai(text: str, out_path: Path) -> None:
    from openai import OpenAI

    client = OpenAI(api_key=config.OPENAI_API_KEY)
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    ) as response:
        response.stream_to_file(out_path)


def generate_tts(text: str, out_path: Path) -> None:
    if config.TTS_PROVIDER == "openai":
        _tts_openai(text, out_path)
    else:
        asyncio.run(_tts_edge(text, out_path))


def _ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def _caption_block_height(num_lines: int) -> int:
    line_spacing = 10
    line_height = CAPTION_FONTSIZE * 1.2 + line_spacing
    return round(num_lines * line_height)


def _render_scene(
    image: Path, audio: Path, caption_file: Path, num_lines: int, duration: float, out_path: Path
) -> None:
    frames = max(1, round(duration * FPS))
    caption_path_escaped = _escape_filter_path(str(caption_file))
    bottom_margin = 100
    caption_y = 1920 - _caption_block_height(num_lines) - bottom_margin
    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
        f"scale=2160:3840,"
        f"zoompan=z='min(zoom+0.0015,1.3)':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},"
        f"drawtext=textfile='{caption_path_escaped}':fontsize={CAPTION_FONTSIZE}:fontcolor=white:"
        f"borderw=4:bordercolor=black@0.7:x=(w-text_w)/2:y={caption_y}:line_spacing=10"
        f"[v]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", "-t", str(duration),
        str(out_path),
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)


def _concat_segments(segments: list[Path], out_path: Path, tmp_dir: Path) -> None:
    list_file = tmp_dir / "concat_list.txt"
    list_file.write_text("".join(f"file '{seg.resolve()}'\n" for seg in segments), encoding="utf-8")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(out_path)]
    subprocess.run(cmd, capture_output=True, text=True, check=True)


def render_video(image_path: Path, scenes: list[dict], out_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="botvideo_") as tmp:
        tmp_dir = Path(tmp)
        segments = []
        for i, scene in enumerate(scenes[:MAX_SCENES]):
            audio_path = tmp_dir / f"scene_{i}.mp3"
            generate_tts(scene["narration"], audio_path)
            duration = _ffprobe_duration(audio_path)

            # drawtext expands "%{...}" even when reading from a textfile, so a lone
            # "%" (e.g. "100%.") must be backslash-escaped or it throws "Stray % near
            # ..." and drops the text for that frame ("%%" does NOT work here).
            caption_text = scene.get("caption", "").replace("%", "\\%")
            wrapped_caption = textwrap.fill(caption_text, width=CAPTION_WRAP_WIDTH)
            caption_file = tmp_dir / f"caption_{i}.txt"
            caption_file.write_text(wrapped_caption, encoding="utf-8")
            num_lines = wrapped_caption.count("\n") + 1

            segment_path = tmp_dir / f"segment_{i}.mp4"
            _render_scene(image_path, audio_path, caption_file, num_lines, duration, segment_path)
            segments.append(segment_path)
        _concat_segments(segments, out_path, tmp_dir)


def run() -> int:
    if not shutil.which("ffmpeg"):
        log.error("ffmpeg not found on PATH — install it (apt/brew install ffmpeg) and retry")
        return 0

    processed = 0
    for path, frontmatter, body in iter_drafts(config.DRAFTS_DIR):
        if frontmatter.get("status") != "image_done":
            continue
        images = frontmatter.get("images") or []
        if not images:
            log.warning("Skipping %s: no image available", path.name)
            continue
        image_path = config.ROOT_DIR / images[0]

        try:
            script = llm.generate_json(
                SCRIPT_SYSTEM_PROMPT, _script_prompt(frontmatter["title"], body), max_tokens=2000
            )
            scenes = script.get("scenes") or []
            if not scenes:
                raise ValueError("LLM returned no scenes")

            video_path = config.VIDEOS_DIR / f"{path.stem}.mp4"
            render_video(image_path, scenes, video_path)

            frontmatter["video"] = str(video_path.relative_to(config.ROOT_DIR))
            frontmatter["status"] = "video_done"
            write_draft(path, frontmatter, body)
            processed += 1
            log.info("Rendered video for: %s (%d scenes)", path.name, len(scenes))
        except Exception as exc:
            log.error("Video render failed for %s: %s", path.name, exc)

    log.info("Bot5 video render: processed %d drafts", processed)
    return processed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    run()
