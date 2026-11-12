#!/usr/bin/env bash
# Kiểm tra ffmpeg/ffprobe đã cài chưa và in hướng dẫn cài nếu thiếu.

if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ ffmpeg đã cài:"
    ffmpeg -version | head -n 1
else
    echo "❌ Chưa cài ffmpeg. Cài bằng:"
    echo "   macOS   : brew install ffmpeg"
    echo "   Ubuntu  : sudo apt update && sudo apt install -y ffmpeg"
    echo "   Windows : choco install ffmpeg   (hoặc tải từ https://ffmpeg.org/download.html)"
    exit 1
fi

if command -v ffprobe >/dev/null 2>&1; then
    echo "✅ ffprobe đã cài"
else
    echo "⚠️  ffprobe không tìm thấy (thường đi kèm ffmpeg, kiểm tra lại cài đặt)"
fi
