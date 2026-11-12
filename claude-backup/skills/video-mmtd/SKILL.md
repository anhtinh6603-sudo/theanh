---
name: video-mmtd
description: Tạo hoặc chỉnh sửa video dọc TikTok, Reels và Shorts dành riêng cho sách Mật Mã Tự Do từ ảnh KOL, ảnh bìa sách, lời thoại hoặc video có sẵn; dùng khi người dùng gọi Video MMTD, $video-mmtd, hoặc yêu cầu tiếp tục series Mật Mã Tự Do. Không dùng cho sách hay chiến dịch không liên quan.
---

# Video MMTD

Tạo video hoàn chỉnh, không dừng ở kịch bản khi người dùng đã yêu cầu làm, xuất hoặc cho xem.

## Đầu ra mặc định

- MP4 H.264/AAC, 1080×1920, 30 fps, 30–50 giây.
- KOL và bìa sách giữ đúng nhận diện từ media người dùng/Drive.
- Nhịp 5 cảnh: hook → vấn đề → cuốn sách → suy ngẫm → CTA.
- Ảnh có push-in 1.00→1.06; chuyển cảnh fade khoảng 0,7 giây.
- Bảng màu than, kem và vàng; chữ tiếng Việt UTF-8.
- Giọng tiếng Việt tự nhiên; ghi rõ là giọng tạm nếu chưa có voice người dùng chọn.
- Karaoke 2–5 từ, word-timing thật, từ đang đọc màu vàng.

## Workflow

1. Ưu tiên media người dùng cung cấp. Nếu được yêu cầu lấy từ Drive, dùng Google Drive để tìm đúng bộ ảnh Mật Mã Tự Do và tải toàn bộ file render về dự án.
2. Trước khi dựng, tạo BRIEF.md, STORYBOARD.md, SCRIPT.md và ledger nguồn media.
3. Đọc [references/workflow.md](references/workflow.md) để chọn cảnh, voice, caption và thông số dựng.
4. Khi dùng Edge TTS, chạy scripts/edge_tts_wordtiming.py để tạo đồng thời audio và JSON word-boundary. Không suy đoán timing từ số chữ.
5. Chạy scripts/build_karaoke_ass.py để tạo caption ASS; không dùng caption nguyên câu dài.
6. Dựng từ media gốc, không chỉnh chồng nhiều lần lên MP4 đã nén nếu vẫn còn ảnh/audio nguồn.
7. Hook phải xuất hiện trong 2 giây đầu. Chỉ thêm CTA khi brief có CTA hoặc người dùng yêu cầu.
8. Trước bàn giao, đọc và thực hiện [references/quality-gates.md](references/quality-gates.md). Sửa mọi lỗi chặn rồi mới xuất.

## Quy tắc bắt buộc

- Không thay KOL, bìa sách hoặc trải nghiệm thật bằng stock/AI không được người dùng chấp thuận.
- Không bịa nội dung sách, số liệu, lời chứng thực hay kết quả tài chính.
- Không để chữ che mắt, miệng, tay hoặc tên sách.
- Không dùng phụ đề dài nhiều dòng. Mỗi cụm 2–5 từ, nằm trong safe zone phía dưới.
- Nếu word-timing không đáng tin cậy, dùng clean captions ngắn hoặc bàn giao bản không karaoke và nói rõ; không giả timing.
- Contact sheet phải gồm midpoint của mọi cảnh và được xem bằng mắt.
- Dùng ffprobe xác minh duration, kích thước, codec, pixel format và audio trước bàn giao.

## Bàn giao

Trả video bằng đường dẫn tuyệt đối, kèm thời lượng, tỷ lệ, codec, nguồn media và voice đã dùng. Có thể kèm contact sheet để người dùng duyệt.
