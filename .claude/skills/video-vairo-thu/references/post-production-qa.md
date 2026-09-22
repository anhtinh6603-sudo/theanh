# Dựng và kiểm tra

## Dựng

- Chuẩn hóa mọi cảnh thành 1080×1920, SAR 1:1, 30 fps trước khi concat.
- Cắt theo `scene_durations`; tổng phải đúng `target_duration`.
- Hard cut là mặc định an toàn cho video hài ngắn. Chỉ dùng dissolve khi nó không làm sai timing thoại.
- Burn file `work/captions.ass` sau khi đã khóa hình và âm thanh.
- Xuất H.264, `yuv420p`, AAC 48 kHz, `faststart`.

## Kiểm tra bắt buộc

1. `ffprobe`: duration, codec, 1080×1920, 30 fps, audio 48 kHz.
2. Giải mã toàn bộ bằng `ffmpeg -v error -i final.mp4 -f null ...`.
3. Đo loudness và true peak.
4. Xem contact sheet trải đều toàn video.
5. Xem hai khung trước/sau mỗi điểm cắt để phát hiện khung đen hoặc nhầm thứ tự.
6. Mở video và nghe ít nhất một lượt hoàn chỉnh trước khi giao.

## Tiêu chí PASS

- thời lượng sai không quá 0.2 giây;
- không lỗi giải mã;
- không khung đen, nhảy cảnh ngoài ý muốn hoặc hình đứng kéo dài;
- phụ đề đúng dấu, đúng nhân vật, không vượt khung;
- thoại không bị cắt, không clip và nghe rõ trên loa điện thoại;
- đường dẫn final tồn tại và file có kích thước hợp lý.

Script `scripts/qc-video.ps1` tạo báo cáo máy và contact sheet; kiểm tra bằng mắt vẫn là bắt buộc.

