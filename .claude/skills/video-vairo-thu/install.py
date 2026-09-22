#!/usr/bin/env python3
"""Cài Video vairo thú cho nhiều nền tảng agent."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


NAME = "video-vairo-thu"
SOURCE = Path(__file__).resolve().parent
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", "qa")


def replace_tree(destination: Path, force: bool, dry_run: bool) -> None:
    source = SOURCE.resolve()
    destination = destination.expanduser().resolve()
    if destination == source or source in destination.parents:
        raise SystemExit(f"Từ chối cài vào bên trong gói nguồn: {destination}")
    if destination.exists() and not force:
        raise SystemExit(f"Đích đã tồn tại: {destination}\nChạy lại với --force nếu muốn thay thế.")
    print(f"Nguồn: {source}\nĐích:  {destination}")
    if dry_run:
        return
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=IGNORE)


def main() -> None:
    parser = argparse.ArgumentParser(description="Cài Video vairo thú cho Claude, Codex, Gemini hoặc Cursor.")
    parser.add_argument("--target", required=True, choices=("claude", "codex", "gemini", "cursor"))
    parser.add_argument("--project", help="Thư mục dự án; bắt buộc với Cursor.")
    parser.add_argument("--force", action="store_true", help="Thay thế bản cài hiện có.")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ in đường dẫn, không ghi file.")
    args = parser.parse_args()

    home = Path.home()
    if args.target == "claude":
        destination = home / ".claude" / "skills" / NAME
    elif args.target == "codex":
        codex_home = Path(os.environ.get("CODEX_HOME", str(home / ".codex")))
        destination = codex_home / "skills" / NAME
    elif args.target == "gemini":
        destination = home / ".gemini" / "extensions" / NAME
    else:
        if not args.project:
            parser.error("--project là bắt buộc khi --target cursor")
        project = Path(args.project).expanduser().resolve()
        destination = project / ".agent-skills" / NAME

    replace_tree(destination, args.force, args.dry_run)

    if args.target == "cursor":
        project = Path(args.project).expanduser().resolve()
        rule_source = SOURCE / "adapters" / "cursor" / "video-vairo-thu.mdc"
        rule_destination = project / ".cursor" / "rules" / "video-vairo-thu.mdc"
        print(f"Rule:  {rule_destination}")
        if not args.dry_run:
            if rule_destination.exists() and not args.force:
                raise SystemExit(f"Rule đã tồn tại: {rule_destination}; dùng --force để thay thế.")
            rule_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(rule_source, rule_destination)

    print("Cài đặt hoàn tất." if not args.dry_run else "Dry run hoàn tất; chưa ghi file.")


if __name__ == "__main__":
    main()
