# Sản xuất bằng Google Flow

## Trước khi tạo

- Đăng nhập đúng tài khoản và mở đúng dự án Flow.
- Tải toàn bộ ảnh cảnh lên một lần nếu được phép.
- Kiểm tra model, tỉ lệ 9:16, thời lượng 8 giây và mức tín dụng cho mỗi clip.
- Tính tổng tín dụng dự kiến. Nếu người dùng chưa phê duyệt rõ tổng chi phí hoặc số clip, dừng ngay trước nút xác nhận tiêu tín dụng và xin phép.

## Mỗi cảnh

1. Chọn đúng ảnh `scene-XX` làm thành phần.
2. Dán prompt chuyển động của cảnh.
3. Kiểm tra prompt chỉ có 1–3 hành động, không yêu cầu thoại/lip-sync/chữ.
4. Bắt đầu tạo và phê duyệt đúng một clip khi đã có quyền.
5. Chờ clip hoàn tất; không gửi trùng lệnh chỉ vì hàng đợi chậm.
6. Mở clip, xem từ đầu đến cuối và kiểm tra khung đầu–giữa–cuối.
7. Tải bản gốc 720p/9:16 và lưu thành `flow/scene-XX.mp4`.

## Tạo lại khi

- nhân vật đổi mặt, đổi tóc, đổi quần áo hoặc đổi loài;
- tay/chân/bàn chân biến dạng rõ;
- đạo cụ biến mất, mọc thêm hoặc đổi hình dạng;
- camera rung, chuyển cảnh ngẫu nhiên, có chữ/logo/watermark;
- không có chuyển động có ý nghĩa.

Ưu tiên sửa prompt và tạo lại riêng cảnh lỗi. Không tạo lại toàn bộ loạt.

## QC nhanh sau tải

- FFprobe: clip 8 giây, H.264, 720×1280 hoặc cao hơn.
- Giải mã clip bằng FFmpeg tới cuối không lỗi.
- Tạo contact sheet ba khung cho mỗi clip và xem bằng mắt trước khi dựng.

