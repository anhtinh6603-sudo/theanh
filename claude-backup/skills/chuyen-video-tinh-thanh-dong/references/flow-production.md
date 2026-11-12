# Sản xuất image-to-video bằng Flow/Omni

## Chuẩn shot

- Tỷ lệ dọc 9:16, chất lượng cao nhất khả dụng; 720p chấp nhận cho cảnh nguồn trước khi upscale.
- Một ảnh tham chiếu chính cho mỗi nhân vật cần khóa nhận diện.
- Một chuyển động chính, một hành động phụ và một chuyển động máy quay nhẹ.
- Shot mở đầu 4–6 giây; các shot nội dung 6–10 giây.

## Prompt khung

Mô tả bối cảnh và hành động cụ thể, sau đó khóa:

`Preserve the exact identity, face, hairstyle, skin tone, body proportions, outfit and product from the reference. Natural eye contact, subtle hand movement, stable anatomy, cinematic light, slow controlled camera movement, vertical 9:16. No extra people, no identity change, no distorted hands, no warped product, no random text or logo.`

Nếu cần typography trong cảnh, cung cấp đúng chuỗi tiếng Việt và yêu cầu không sinh thêm chữ. Với nội dung cần phụ đề, ưu tiên tạo video không chữ rồi thêm phụ đề ở khâu dựng.

## Cổng duyệt từng cảnh

- Xem từ đầu đến cuối ở tốc độ bình thường.
- Khuôn mặt không đổi người hoặc méo.
- Tay, tóc, trang phục và sản phẩm không biến dạng.
- Chuyển động có chủ đích, không rung giật.
- Crop không cắt mắt, cằm, tay hoặc sản phẩm chính.
- Không có chữ rác, watermark mới hoặc logo tự sinh.

Không tải hoặc ghép cảnh chưa đạt. Tạo lại với chuyển động đơn giản hơn nếu nhận diện không ổn.

## Lấy clip từ Flow

Xác nhận mục đang chọn có trình phát video và thời lượng, không chỉ có ảnh xem trước. Khi nút tải xuống trả về ảnh, quay lại chọn đúng asset video. Giữ mỗi clip nguồn dưới tên ổn định như `scene-01.mp4`, `scene-02.mp4`.

## Dựng master

1. Lập danh sách clip và kiểm tra codec, kích thước, fps, thời lượng.
2. Bỏ audio Flow nếu dùng narration riêng.
3. Scale/crop giữ tỷ lệ, không kéo méo.
4. Dùng fade hoặc crossfade 0,15–0,35 giây khi phù hợp.
5. Đồng nhất tương phản, saturation và độ nét nhẹ; tránh làm da giả.
6. Dùng gradient tối nhẹ cho phụ đề. Không dùng khối đen lớn nếu không cần.
7. Đặt CTA ngắn ở cuối khi kịch bản có CTA.
8. Kiểm tra frame ở đầu, giữa, cuối và mọi điểm chuyển cảnh trước khi bàn giao.

