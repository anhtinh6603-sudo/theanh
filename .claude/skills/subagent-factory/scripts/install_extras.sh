#!/usr/bin/env bash
# Cài nền kỹ thuật edit nâng cao cho Công xưởng Subagent (chạy lại được, idempotent).
# Container cloud là tạm thời: chạy script này đầu mỗi phiên mới hoặc đưa vào setup script của môi trường.
set -u
TOOLS=/opt/subagent-tools
mkdir -p "$TOOLS" ~/.u2net

echo "== rembg (xóa nền)"
python3 -c "import rembg" 2>/dev/null || pip3 install --break-system-packages -q "rembg[cpu,cli]"
[ -s ~/.u2net/u2net.onnx ] || curl -sSL -o ~/.u2net/u2net.onnx \
  https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx

echo "== whisper.cpp (phụ đề tự động)"
if [ ! -x "$TOOLS/whisper.cpp/build/bin/whisper-cli" ]; then
  [ -d "$TOOLS/whisper.cpp" ] || git clone -q --depth 1 https://github.com/ggml-org/whisper.cpp "$TOOLS/whisper.cpp"
  cmake -S "$TOOLS/whisper.cpp" -B "$TOOLS/whisper.cpp/build" -DCMAKE_BUILD_TYPE=Release >/dev/null
  cmake --build "$TOOLS/whisper.cpp/build" -j"$(nproc)" --config Release >/dev/null
fi
MODEL="$TOOLS/whisper.cpp/models/ggml-medium.bin"
if [ ! -s "$MODEL" ]; then
  # Model nằm trên huggingface.co - cần mạng môi trường cho phép host này.
  curl -fsSL -o "$MODEL" https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin \
    || { rm -f "$MODEL"; echo "  ⚠️  không tải được model whisper (huggingface.co bị chặn?)"; }
fi

echo "== content-bot-system"
pip3 install --break-system-packages -q -r "$(git rev-parse --show-toplevel)/content-bot-system/requirements.txt"

echo "Xong. Real-ESRGAN: xem mục 'Nền kỹ thuật' trong PHIEU_DE_XUAT.md (cần chủ cho phép chạy binary)."
