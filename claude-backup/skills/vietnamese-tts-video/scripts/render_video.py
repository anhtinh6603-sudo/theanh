#!/usr/bin/env python3
"""
render_video.py  -  Free, no-API-key, no-captcha renderer for vertical (9:16)
Vietnamese talking-photo videos: one real still image + AI narration + burned
Vietnamese captions.

This exists because the exact ffmpeg incantation that makes Vietnamese
captions render at the RIGHT size (instead of exploding to fill the screen
and covering the subject's face) is not obvious and is easy to get wrong.
See references/ffmpeg-gotchas.md for the story. This script encodes the
working recipe so you don't have to rediscover it.

Requires on PATH: ffmpeg, ffprobe, python -m pip install edge-tts

Usage:
  python render_video.py \
      --image path/to/real_reference_photo.png \
      --narration path/to/narration.txt \
      --out path/to/output.mp4 \
      --voice vi-VN-NamMinhNeural \
      [--rate +0%] [--fps 30] [--width 1080] [--height 1920] \
      [--font Arial] [--font-size 50] [--align bottom] [--zoom 1.06] \
      [--qc-frames 4]

What it does, in order:
  1. Calls edge-tts to synthesize narration.mp3 + narration.srt (word/line
     timed). Retries automatically  -  edge-tts occasionally fails a single
     call with "NoAudioReceived" for no real reason; a retry almost always
     fixes it.
  2. Converts the SRT to ASS with ffmpeg, then PATCHES the ASS file's
     PlayResX/PlayResY and Style line directly (see gotcha doc). This is
     the step that actually controls caption size/position correctly.
  3. Reads the real audio duration and computes the exact frame count so
     the Ken Burns zoompan animation and the final -t duration match the
     narration exactly (no silent tail, no early cutoff).
  4. Renders the real photo with a slow zoompan push-in, burns the fixed
     ASS captions on top, muxes the narration audio, encodes H.264/AAC.
  5. Runs ffprobe to confirm duration/streams, then extracts N evenly
     spaced frames as JPGs and prints their paths so you (Claude) can
     Read() each one and eyeball it before telling the user it's done  - 
     script output alone does not prove the captions look right on screen.

This script does not touch or bypass any CAPTCHA. If you need a TTS voice
that requires one (e.g. a browser-based free TTS site), stop and ask the
user to do that step manually  -  see the skill's SKILL.md.
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def synthesize_tts(narration_path: Path, voice: str, rate: str, out_mp3: Path, out_srt: Path, retries: int = 3):
    """edge-tts occasionally fails a single call transiently. Retry before giving up."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            run([
                sys.executable, "-m", "edge_tts",
                "-f", str(narration_path),
                "-v", voice,
                "--rate", rate,
                "--write-media", str(out_mp3),
                "--write-subtitles", str(out_srt),
            ])
            if out_mp3.exists() and out_mp3.stat().st_size > 0:
                return
        except subprocess.CalledProcessError as e:
            last_err = e
            print(f"[retry {attempt}/{retries}] edge-tts failed: {e.stderr.strip()[-300:]}", file=sys.stderr)
            time.sleep(2)
    raise RuntimeError(
        "edge-tts failed after retries. This voice/network combo may be down. "
        "Try again in a bit, try the other vi-VN voice, or fall back to asking "
        "the user for a manually-generated audio file."
    ) from last_err


def srt_to_fixed_ass(srt_path: Path, ass_path: Path, width: int, height: int,
                      font: str, font_size: int, align: str, margin_v: int):
    """Convert SRT -> ASS via ffmpeg, then patch PlayRes + Style so captions
    render at the correct physical size instead of exploding to fill the
    frame (see references/ffmpeg-gotchas.md)."""
    run(["ffmpeg", "-y", "-v", "error", "-i", str(srt_path), str(ass_path)])
    text = ass_path.read_text(encoding="utf-8")

    text = re.sub(r"PlayResX:\s*\d+", f"PlayResX: {width}", text)
    text = re.sub(r"PlayResY:\s*\d+", f"PlayResY: {height}", text)

    # ASS alignment numpad values: 2 = bottom-center, 8 = top-center, 5 = middle-center
    align_map = {"bottom": 2, "top": 8, "middle": 5}
    align_val = align_map.get(align, 2)

    margin_lr = max(40, width // 16)
    style_line = (
        f"Style: Default,{font},{font_size},&H00FFFFFF,&H00FFFFFF,"
        f"&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,"
        f"{align_val},{margin_lr},{margin_lr},{margin_v},1"
    )
    text = re.sub(r"Style: Default,.*", style_line, text)
    ass_path.write_text(text, encoding="utf-8")


def probe_duration(path: Path) -> float:
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ]).stdout.strip()
    return float(out)


def build_video(image: Path, audio: Path, ass: Path, out: Path,
                 width: int, height: int, fps: int, zoom_max: float, duration: float):
    frame_count = max(1, round(duration * fps))
    zoom_step = max(0.0000001, (zoom_max - 1.0) / frame_count)
    # Scale up 2x before zoompan so the push-in has resolution headroom.
    up_w, up_h = width * 2, height * 2

    ass_arg = str(ass).replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},scale={up_w}:{up_h},"
        f"zoompan=z='min(zoom+{zoom_step},{zoom_max})':d={frame_count}:s={width}x{height}:fps={fps}[bg];"
        f"[bg]subtitles='{ass_arg}'[v]"
    )

    run([
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-t", f"{duration:.3f}", "-r", str(fps),
        str(out),
    ], cwd=str(ass.parent))


def extract_qc_frames(video: Path, out_dir: Path, duration: float, count: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(count):
        # Sample interior points, never frame 0 or the very last frame.
        ts = duration * (i + 1) / (count + 1)
        p = out_dir / f"qc_{ts:05.1f}s.jpg"
        run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-ss", f"{ts:.2f}",
             "-update", "1", "-frames:v", "1", str(p)])
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--image", required=True, type=Path, help="Real reference photo (KOL/product), portrait-ish.")
    ap.add_argument("--narration", required=True, type=Path, help="Plain-text file with the Vietnamese narration.")
    ap.add_argument("--out", required=True, type=Path, help="Output .mp4 path.")
    ap.add_argument("--voice", default="vi-VN-NamMinhNeural",
                     help="edge-tts voice. vi-VN-NamMinhNeural (male) or vi-VN-HoaiMyNeural (female).")
    ap.add_argument("--rate", default="+0%", help="edge-tts speaking rate delta, e.g. +8%% to speak faster.")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1920)
    ap.add_argument("--font", default="Arial", help="Must be installed system-wide and cover Vietnamese diacritics.")
    ap.add_argument("--font-size", type=int, default=50, help="Tuned for 1080-wide canvas; scale roughly with width.")
    ap.add_argument("--align", choices=["bottom", "top", "middle"], default="bottom",
                     help="bottom is safest  -  least likely to cover the subject's face.")
    ap.add_argument("--margin-v", type=int, default=220, help="Vertical margin in px from the aligned edge.")
    ap.add_argument("--zoom", type=float, default=1.06, help="Final Ken Burns zoom level (starts at 1.0).")
    ap.add_argument("--qc-frames", type=int, default=4, help="How many frames to extract for visual QC.")
    args = ap.parse_args()

    work = args.out.parent
    work.mkdir(parents=True, exist_ok=True)
    voice_mp3 = work / "_tts_voice.mp3"
    voice_srt = work / "_tts_voice.srt"
    voice_ass = work / "_tts_voice.ass"

    print("== 1/5 Synthesizing narration (edge-tts, free, no key, no captcha) ==", file=sys.stderr)
    synthesize_tts(args.narration, args.voice, args.rate, voice_mp3, voice_srt)

    print("== 2/5 Converting SRT -> ASS and patching PlayRes/Style ==", file=sys.stderr)
    srt_to_fixed_ass(voice_srt, voice_ass, args.width, args.height,
                      args.font, args.font_size, args.align, args.margin_v)

    print("== 3/5 Measuring narration duration ==", file=sys.stderr)
    duration = probe_duration(voice_mp3)
    print(f"   duration = {duration:.3f}s", file=sys.stderr)

    print("== 4/5 Rendering video (Ken Burns + burned captions + audio) ==", file=sys.stderr)
    build_video(args.image, voice_mp3, voice_ass, args.out,
                args.width, args.height, args.fps, args.zoom, duration)

    print("== 5/5 Verifying output + extracting QC frames ==", file=sys.stderr)
    out_duration = probe_duration(args.out)
    qc_dir = work / "qc_frames"
    frames = extract_qc_frames(args.out, qc_dir, out_duration, args.qc_frames)

    print("\nDONE.")
    print(f"video: {args.out}  (duration {out_duration:.2f}s)")
    print("QC frames  -  Read() every one of these and check before telling the user it's finished:")
    for f in frames:
        print(f"  {f}")
    print(
        "\nChecklist while looking at the frames:\n"
        "  - Vietnamese diacritics render correctly (no boxes/mojibake/missing marks)\n"
        "  - caption text fits fully on screen, no line cut off at top/bottom\n"
        "  - caption does not cover the subject's face or the product\n"
        "  - background image isn't stretched/distorted\n"
        "If anything looks wrong, it's almost always --font-size too big for --width, "
        "or --align/--margin-v pushing multi-line text off-screen. See "
        "references/ffmpeg-gotchas.md."
    )


if __name__ == "__main__":
    main()
