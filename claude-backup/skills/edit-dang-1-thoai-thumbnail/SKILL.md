---
name: "edit-dang-1-thoai-thumbnail"
description: "Edit Dạng 1: video talking-head dọc 9:16 cắt gọn tự nhiên + thumbnail tiêu đề mở đầu + caption động theo lời nói. Dùng khi khách nói \"edit Dạng 1 cho video này\"."
---

# Dạng 1 — Thoại + Thumbnail mở đầu (nền tảng)

## Sản phẩm
1 người nói trước camera → video ngắn dọc 9:16, cắt gọn tự nhiên, mở đầu bằng thumbnail/thẻ tiêu đề AI viết theo nội dung, caption động chạy theo lời nói. Nền cho Dạng 2/3/4.

## Công cụ
- ffmpeg (silencedetect, crop, overlay chữ)
- Whisper (faster-whisper) với word-level timestamps
- hyperframes (composition HTML/CSS, seek-safe) cho chữ động/thumbnail; nếu không có thì dùng app web "Video Studio" hoặc ffmpeg drawtext

## Quy trình
1. Transcribe cấp câu: Whisper word_timestamps=True, cố định ngôn ngữ vi.
2. Auto-cut: `ffmpeg -af silencedetect=noise=-25dB:d=0.4`, chỉ cắt lặng ≥0.6s; cắt từ đệm (ừm, à, kiểu như), câu vấp (giữ bản tốt nhất), rác đầu/cuối. Jump cut dứt khoát, cắt tại điểm hết ý, 2 điểm cắt <0.4s thì gộp, chừa ≥0.15s đệm, không cắt quá 40% thời lượng. Cắt xong MỚI transcribe lại — mọi mốc thời gian lấy từ bản đã cắt.
3. Thumbnail mở đầu (2-3s): chọn 1 trong 6 bố cục — stack_hierarchy (bán hàng/tuyên bố mạnh), magazine (series/tập), serif_mix (câu hỏi/chia sẻ trí tuệ), lifestyle (vlog), brand_word (1 từ thương hiệu lớn), spaced_caps (studio/agency). title 4-9 từ viết lại cho tò mò, không copy câu chào; accent = 1 cụm nằm nguyên văn trong title, tô màu nhấn.
4. Caption động: chữ trắng dày, 1-3 từ/cụm, khớp word-timestamps, đặt dưới 1/3 khung, không che mặt.
5. Dựng: track video + track thumbnail + track caption.

## Xuất
9:16 1080×1920, giữ audio gốc, nhạc nền tuỳ khách. File: output/<tên>-dang1.mp4

## Không có trong Dạng 1
Không zoom cảm xúc, không overlay minh hoạ, không crop bám mặt, không infographic (đó là Dạng 2/3/4).

## Cài đặt (1 lần)
- ffmpeg: winget install Gyan.FFmpeg / brew install ffmpeg / apt install ffmpeg
- Python 3.10+: `pip install faster-whisper librosa numpy opencv-python mediapipe` (CPU dùng model small/medium)
- Node ≥18 + hyperframes (chạy `hyperframes doctor`)
- Thư mục: input/, output/, assets/{sfx,music,fonts,icons,luts}/
- Xác nhận: `ffmpeg -version`, `python -c "import faster_whisper, librosa, cv2, mediapipe"`, `node --version` đều chạy không lỗi mới dựng.

## Tài nguyên
- Font: Google Fonts (Be Vietnam Pro / Inter có dấu tiếng Việt) tải về assets/fonts/.
- Nhạc trend có bản quyền: KHÔNG tự tải, khách tự cung cấp file hoặc gợi ý nhạc free-license.
- Khách cung cấp: video gốc (bắt buộc), màu thương hiệu + logo (tuỳ chọn; mặc định trắng/vàng nhấn).

## Khách chỉ cần
Đưa video vào input/ và nói "edit Dạng 1 cho video này". Agent tự kiểm môi trường → tải font → transcribe → cắt → viết thumbnail → dựng → xuất → báo đường dẫn.

## App không cần cài
Nếu máy khách không cài được gì: dùng app web "Video Studio Dạng 1·2" (Claude đã dựng, chạy trên trình duyệt điện thoại/máy tính).