#!/usr/bin/env python3
"""Tạo cấu trúc dự án Video vairo thú từ template."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tạo dự án Video vairo thú mới.")
    parser.add_argument("--project", required=True, help="Thư mục dự án mới.")
    parser.add_argument("--title", required=True, help="Tên tập/video.")
    args = parser.parse_args()

    target = Path(args.project).expanduser().resolve()
    if target.parent == target:
        raise SystemExit("Từ chối dùng thư mục gốc làm dự án.")
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Thư mục đích không rỗng: {target}")

    template = Path(__file__).resolve().parents[1] / "assets" / "project-template"
    target.mkdir(parents=True, exist_ok=True)
    for item in template.iterdir():
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            text = item.read_text(encoding="utf-8").replace("{{TITLE}}", args.title)
            destination.write_text(text, encoding="utf-8")
    for folder in ("images", "flow", "audio", "music", "sfx", "work", "qa"):
        (target / folder).mkdir(exist_ok=True)
    caption = target / "captions.ass"
    if caption.exists():
        caption.replace(target / "work" / "captions.ass")
    print(f"Đã tạo dự án: {target}")


if __name__ == "__main__":
    main()
