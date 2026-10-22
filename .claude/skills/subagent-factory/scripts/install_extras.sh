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

echo "== Real-ESRGAN (làm nét) - chủ cho phép 2026-10-22"
if [ ! -x "$TOOLS/realesrgan/realesrgan-ncnn-vulkan" ]; then
  DEBIAN_FRONTEND=noninteractive apt-get install -y -q mesa-vulkan-drivers libvulkan1 libgomp1 >/dev/null 2>&1 \
    || { apt-get update -q >/dev/null 2>&1 && DEBIAN_FRONTEND=noninteractive apt-get install -y -q mesa-vulkan-drivers libvulkan1 libgomp1 >/dev/null 2>&1; }
  [ -s "$TOOLS/esrgan.zip" ] || curl -sSL -o "$TOOLS/esrgan.zip" \
    https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
  mkdir -p "$TOOLS/realesrgan"
  python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$TOOLS/esrgan.zip" "$TOOLS/realesrgan"
  chmod +x "$TOOLS/realesrgan/realesrgan-ncnn-vulkan"
fi

echo "== content-bot-system"
pip3 install --break-system-packages -q -r "$(git rev-parse --show-toplevel)/content-bot-system/requirements.txt"

echo "Xong."
