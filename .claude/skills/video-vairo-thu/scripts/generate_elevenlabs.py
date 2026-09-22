#!/usr/bin/env python3
"""Tạo từng lượt thoại ElevenLabs bằng Python stdlib."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tạo thoại từ takes.json qua ElevenLabs.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--takes", default="takes.json")
    parser.add_argument("--api-key-env", default="ELEVENLABS_API_KEY")
    parser.add_argument("--model", default="eleven_v3")
    parser.add_argument("--language", default="vi")
    parser.add_argument("--output-format", default="mp3_44100_128")
    parser.add_argument("--dry-run", action="store_true", help="Kiểm tra cấu hình, không gọi API.")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    takes_path = root / args.takes
    if not takes_path.is_file():
        raise SystemExit(f"Không tìm thấy {takes_path}")
    takes = json.loads(takes_path.read_text(encoding="utf-8-sig"))
    if not isinstance(takes, list) or not takes:
        raise SystemExit("takes.json phải là một danh sách không rỗng.")

    api_key = os.environ.get(args.api_key_env)
    errors: list[str] = []
    resolved: list[tuple[dict, str]] = []
    for index, take in enumerate(takes, 1):
        voice_id = take.get("voice_id") or os.environ.get(str(take.get("voice_env", "")))
        if not take.get("file") or not take.get("text"):
            errors.append(f"Take {index}: thiếu file hoặc text")
        if not voice_id:
            errors.append(f"Take {index}: thiếu voice_id/biến {take.get('voice_env')}")
        resolved.append((take, voice_id or ""))
    if not api_key:
        errors.append(f"Thiếu biến môi trường {args.api_key_env}")
    if errors:
        raise SystemExit("Cấu hình chưa hợp lệ:\n- " + "\n- ".join(errors))
    if args.dry_run:
        print(f"PASS: {len(takes)} take hợp lệ; chưa gọi API.")
        return

    audio_root = root / "audio"
    audio_root.mkdir(parents=True, exist_ok=True)
    for take, voice_id in resolved:
        encoded_voice = urllib.parse.quote(voice_id, safe="")
        encoded_format = urllib.parse.quote(args.output_format, safe="")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{encoded_voice}/with-timestamps?output_format={encoded_format}"
        payload = {
            "text": str(take["text"]),
            "model_id": args.model,
            "language_code": args.language,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.78, "style": 0.30, "use_speaker_boost": True},
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise SystemExit(f"ElevenLabs trả lỗi HTTP {exc.code} cho {take['file']}: {detail}") from exc
        stem = str(take["file"])
        (audio_root / f"{stem}.mp3").write_bytes(base64.b64decode(result["audio_base64"]))
        alignment = result.get("normalized_alignment") or result.get("alignment") or {}
        (audio_root / f"{stem}-alignment.json").write_text(
            json.dumps(alignment, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Đã tạo audio/{stem}.mp3")


if __name__ == "__main__":
    main()
