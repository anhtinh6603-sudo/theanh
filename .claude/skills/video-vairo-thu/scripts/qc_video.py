#!/usr/bin/env python3
"""Kiểm tra kỹ thuật video và tạo contact sheet."""

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


def run(command: list[str], capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=capture)


def main() -> None:
    parser = argparse.ArgumentParser(description="QC file MP4 Video vairo thú.")
    parser.add_argument("--video", required=True)
    parser.add_argument("--expected-duration", type=float, default=0)
    args = parser.parse_args()
    for name in ("ffmpeg", "ffprobe"):
        if not shutil.which(name):
            raise SystemExit(f"{name} chưa có trong PATH.")

    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        raise SystemExit(f"Không tìm thấy {video}")
    qa = video.parent / "qa"
    qa.mkdir(exist_ok=True)
    probe_result = run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,bit_rate:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
        "-of", "json", str(video),
    ], capture=True)
    probe = json.loads(probe_result.stdout)
    video_stream = next((stream for stream in probe["streams"] if stream.get("codec_type") == "video"), {})
    audio_stream = next((stream for stream in probe["streams"] if stream.get("codec_type") == "audio"), {})
    duration = float(probe["format"]["duration"])

    decode = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"],
        text=True, capture_output=True,
    )
    decode_errors = decode.stderr.strip()
    decode_ok = decode.returncode == 0 and not decode_errors
    audio = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-",
    ], capture=True)
    loudness_matches = re.findall(r"I:\s+(-?\d+(?:\.\d+)?)\s+LUFS", audio.stderr)
    peak_matches = re.findall(r"Peak:\s+(-?\d+(?:\.\d+)?)\s+dBFS", audio.stderr)
    loudness = float(loudness_matches[-1]) if loudness_matches else None
    true_peak = float(peak_matches[-1]) if peak_matches else None

    contact_sheet = qa / "final-contact-sheet.jpg"
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf",
        f"fps=12/{duration:g},scale=270:480,tile=4x3:padding=6:margin=6", "-frames:v", "1", str(contact_sheet),
    ])

    duration_ok = args.expected_duration <= 0 or abs(duration - args.expected_duration) <= 0.2
    format_ok = (
        video_stream.get("codec_name") == "h264" and int(video_stream.get("width", 0)) == 1080
        and int(video_stream.get("height", 0)) == 1920 and video_stream.get("r_frame_rate") == "30/1"
        and audio_stream.get("codec_name") == "aac" and int(audio_stream.get("sample_rate", 0)) == 48000
    )
    audio_ok = loudness is not None and -16.5 <= loudness <= -13.5 and true_peak is not None and true_peak <= -1.5
    status = "PASS" if duration_ok and format_ok and decode_ok and audio_ok else "FAIL"
    report = {
        "status": status, "video": str(video), "duration": round(duration, 3),
        "expected_duration": args.expected_duration or None, "video_codec": video_stream.get("codec_name"),
        "width": video_stream.get("width"), "height": video_stream.get("height"), "fps": video_stream.get("r_frame_rate"),
        "pixel_format": video_stream.get("pix_fmt"), "audio_codec": audio_stream.get("codec_name"),
        "sample_rate": audio_stream.get("sample_rate"), "channels": audio_stream.get("channels"),
        "integrated_lufs": loudness, "true_peak_dbfs": true_peak, "decode_ok": decode_ok,
        "decode_errors": decode_errors, "contact_sheet": str(contact_sheet), "visual_review_required": True,
    }
    report_path = qa / "qc-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Báo cáo: {report_path}")
    print("Hãy xem contact sheet và toàn bộ video bằng mắt/tai trước khi giao.")


if __name__ == "__main__":
    main()
