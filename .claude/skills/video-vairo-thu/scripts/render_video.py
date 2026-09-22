#!/usr/bin/env python3
"""Dựng video dọc từ clip Flow, audio, timeline và phụ đề ASS."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def run(command: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=capture)


def require_tools() -> None:
    for name in ("ffmpeg", "ffprobe"):
        if not shutil.which(name):
            raise SystemExit(f"{name} chưa có trong PATH.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dựng final.mp4 cho Video vairo thú.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--timeline", default="timeline.json")
    parser.add_argument("--output", default="final.mp4")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ kiểm tra đầu vào.")
    args = parser.parse_args()
    require_tools()

    root = Path(args.project).expanduser().resolve()
    timeline_path = root / args.timeline
    caption_path = root / "work" / "captions.ass"
    if not timeline_path.is_file() or not caption_path.is_file():
        raise SystemExit("Thiếu timeline.json hoặc work/captions.ass.")
    timeline = json.loads(timeline_path.read_text(encoding="utf-8-sig"))
    target = float(timeline["target_duration"])
    durations = [float(value) for value in timeline["scene_durations"]]
    scenes = sorted((root / "flow").glob("scene-*.mp4"))
    if len(scenes) != len(durations) or not scenes:
        raise SystemExit(f"Số clip Flow ({len(scenes)}) phải bằng số scene_durations ({len(durations)}).")
    if abs(sum(durations) - target) > 0.01:
        raise SystemExit("Tổng scene_durations khác target_duration.")
    tracks = timeline.get("audio_tracks") or []
    bgm = timeline.get("bgm")
    if not tracks and not bgm:
        raise SystemExit("timeline.json chưa có audio_tracks hoặc bgm.")
    for track in tracks:
        if not (root / track["file"]).is_file():
            raise SystemExit(f"Thiếu audio: {track['file']}")
    if bgm and not (root / bgm["file"]).is_file():
        raise SystemExit(f"Thiếu BGM: {bgm['file']}")
    if args.dry_run:
        print(f"PASS: {len(scenes)} cảnh, tổng {target:g}s, {len(tracks)} track thoại.")
        return

    work = root / "work"
    work.mkdir(exist_ok=True)
    video_base = work / "video-base.mp4"
    video_command = ["ffmpeg", "-y", "-loglevel", "error"]
    for scene in scenes:
        video_command += ["-i", str(scene)]
    filters: list[str] = []
    labels = ""
    for index, duration in enumerate(durations):
        filters.append(
            f"[{index}:v]trim=duration={duration:g},setpts=PTS-STARTPTS,"
            f"scale=1080:1920:flags=lanczos,setsar=1,fps=30[v{index}]"
        )
        labels += f"[v{index}]"
    filters.append(f"{labels}concat=n={len(scenes)}:v=1:a=0[v]")
    video_command += [
        "-filter_complex", ";".join(filters), "-map", "[v]", "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video_base),
    ]
    run(video_command)

    audio_raw = work / "audio-raw.wav"
    audio_mix = work / "audio-mix.wav"
    audio_command = ["ffmpeg", "-y", "-loglevel", "error"]
    audio_filters: list[str] = []
    audio_labels: list[str] = []
    input_index = 0
    for track in tracks:
        audio_command += ["-i", str(root / track["file"])]
        start = int(track.get("start_ms", 0))
        volume = float(track.get("volume", 1.0))
        label = f"a{input_index}"
        audio_filters.append(f"[{input_index}:a]adelay={start}|{start},volume={volume:g}[{label}]")
        audio_labels.append(f"[{label}]")
        input_index += 1
    if bgm:
        audio_command += ["-stream_loop", "-1", "-i", str(root / bgm["file"])]
        volume = float(bgm.get("volume", 0.10))
        fade_start = max(0.0, target - 2.0)
        audio_filters.append(
            f"[{input_index}:a]atrim=duration={target:g},asetpts=PTS-STARTPTS,volume={volume:g},"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_start:g}:d=2[bgm]"
        )
        audio_labels.append("[bgm]")
    audio_filters.append(
        f"{''.join(audio_labels)}amix=inputs={len(audio_labels)}:duration=longest:dropout_transition=0,"
        f"apad=pad_dur={target:g},atrim=duration={target:g},aresample=48000[raw]"
    )
    audio_command += [
        "-filter_complex", ";".join(audio_filters), "-map", "[raw]", "-ac", "2", "-ar", "48000",
        "-c:a", "pcm_s16le", str(audio_raw),
    ]
    run(audio_command)

    analysis = run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(audio_raw), "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture=True,
    )
    matches = re.findall(r"I:\s+(-?\d+(?:\.\d+)?)\s+LUFS", analysis.stderr)
    if not matches:
        raise SystemExit("Không đo được loudness của audio.")
    gain = -15.0 - float(matches[-1])
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(audio_raw), "-af", f"volume={gain:g}dB,alimiter=limit=0.84",
        "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", str(audio_mix),
    ])

    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", "work/video-base.mp4", "-i", "work/audio-mix.wav",
        "-vf", "subtitles=work/captions.ass", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", "-t", f"{target:g}", "-movflags", "+faststart", str(output),
    ], cwd=root)
    print(f"Đã xuất: {output}")
    probe = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels", "-of", "json", str(output),
    ], capture=True)
    print(probe.stdout)


if __name__ == "__main__":
    main()
