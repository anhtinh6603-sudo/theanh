---
name: chuyen-video-tinh-thanh-dong
description: Biến một hoặc nhiều ảnh tĩnh thành video dọc có chuyển động, giữ nhận diện nhân vật và sản phẩm, sau đó ghép cảnh, đồng bộ lời thoại, làm phụ đề và xuất final master cho TikTok, Reels hoặc Shorts. Dùng khi người dùng gọi “Chuyển Video Tĩnh Thành Động”, $chuyen-video-tinh-thanh-dong, muốn image-to-video bằng Flow/Omni hoặc muốn ghép các cảnh đã tạo thành video hoàn chỉnh. Không dùng cho video ngang dài, hoạt hình không dựa trên ảnh hoặc yêu cầu chỉ chỉnh một ảnh tĩnh.
---

# Chuyển Video Tĩnh Thành Động

Tạo sản phẩm cuối là MP4 phát được, không dừng ở prompt hay storyboard khi người dùng đã yêu cầu làm video.

## Đầu vào

- Một hoặc nhiều ảnh tham chiếu của nhân vật, sản phẩm hoặc bối cảnh.
- Kịch bản, lời thoại hoặc mục tiêu nội dung.
- Video/âm thanh có sẵn nếu người dùng muốn giữ giọng hay nhạc gốc.
- Thời lượng và nền tảng; nếu thiếu, mặc định dọc 9:16, 30–45 giây.

Không tự thay ảnh tham chiếu bằng người hoặc sản phẩm khác. Nếu thiếu ảnh bắt buộc, yêu cầu người dùng cung cấp.

## Quy trình

1. Phân tích kịch bản thành các shot 4–10 giây, mỗi shot chỉ có một hành động chính.
2. Viết `BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md` và bảng nguồn media trước khi tạo.
3. Khi dùng Flow/Omni, đọc [references/flow-production.md](references/flow-production.md).
4. Tạo thử một shot trước. Chỉ tiếp tục hàng loạt khi khuôn mặt, tóc, da, trang phục, tay và sản phẩm ổn định.
5. Xem toàn bộ từng clip, không chỉ thumbnail. Loại cảnh có mặt trôi, tay méo, vật thể đổi hình, chữ rác hoặc crop sai.
6. Tải đúng tệp video MP4 về dự án; không nhầm ảnh thumbnail với video.
7. Chuẩn hóa mọi cảnh về 1080×1920, 30 fps, SAR 1:1. Tắt âm thanh sinh tự động nếu đã có lời thoại chính.
8. Ghép cảnh theo mạch hook → nội dung → kết luận/CTA. Dùng chuyển cảnh ngắn, màu đồng nhất và chuyển động vừa phải.
9. Đồng bộ lời thoại từ audio sạch nhất. Phụ đề phải dựa trên timing thật, cụm 2–5 từ, tiếng Việt đúng dấu và nằm trong vùng an toàn.
10. Nếu clip Flow đã có chữ sai hoặc caption sinh tự động, ưu tiên tạo lại cảnh sạch. Khi không thể tạo lại, che tối nhẹ vùng chữ và đặt phụ đề đúng; không để hai lớp chữ cạnh tranh.
11. Chuẩn hóa âm thanh khoảng −14 LUFS, true peak không quá −1.5 dB; giữ lời rõ hơn nhạc nền.
12. Xuất H.264/AAC, `faststart`, rồi kiểm tra bằng `ffprobe`, contact sheet và các frame tại điểm chuyển cảnh.

## Tiêu chuẩn final master

- Hook rõ trong hai giây đầu.
- Nhân vật và đạo cụ đồng nhất giữa các shot.
- Không có chữ rác, lỗi dấu, cảnh đen, khung hình đóng băng hoặc audio bị cắt.
- Phụ đề không che mắt, miệng, bàn tay hay sản phẩm.
- Video và audio lệch thời lượng không quá 0,25 giây.
- Bàn giao đường dẫn MP4 tuyệt đối, thời lượng, độ phân giải và các nguồn chính.

Không đăng video, xóa bản gốc hoặc tạo thêm cảnh có chi phí nếu người dùng chưa cho phép hành động đó.
