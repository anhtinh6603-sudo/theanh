# Playbook điều khiển Flow từ đầu tới cuối

## Những gì người dùng đã thiết lập

1. Người dùng chọn hoặc tạo một project Flow làm không gian sản xuất chính, rồi lưu URL trong `user-config.md`.
2. Tạo/lưu avatar và nhân vật làm component để giữ nhận diện tốt hơn mô tả bằng chữ; lưu tên hiển thị và alias sau khi người dùng xác nhận.
3. Chốt cấu hình sản xuất: Video → Thành phần → Omni 1.1 Flash → 9:16 → chất lượng cao nhất (đã kiểm chứng là 720p) → 10 giây → x1.
4. Chốt mỹ thuật: TVC không thoại; sang trọng, đẹp, lịch lãm, giàu cảm xúc; 2–3 góc quay điện ảnh; phần lớn là medium-close/close-up.
5. Chốt khóa trang phục cho từng avatar nếu người dùng yêu cầu và lưu trong `user-config.md`.
6. Qua các lượt thử, bổ sung quy tắc khóa bối cảnh, khóa tư thế/hành động, giao tiếp ánh mắt, micro-expression, chuyển động vòng cung nhẹ và câu chuyện tiếp diễn tới khung hình cuối.
7. Đầu ra phải được phát và kiểm tra thực tế; không suy luận chất lượng chỉ từ prompt hoặc ảnh thumbnail.

## Cách gọi nhanh

Người dùng chỉ cần gọi `$flow-tvc-director` kèm một câu ý tưởng, ví dụ: `Tạo TVC tôi và nhân vật chính đi giữa thảo nguyên Mông Cổ lúc hoàng hôn`.

Nếu brief đã có đủ chủ thể, hành động và bối cảnh, không hỏi lại. Tự dùng mặc định đã xác nhận. Chỉ hỏi khi thiếu tài sản bắt buộc, chưa đăng nhập, project không truy cập được hoặc lựa chọn mới có thể làm thay đổi đáng kể ý định.

## Trình tự tự động

1. Mở trình duyệt trong ứng dụng và truy cập project đã lưu nếu chưa mở.
2. Quan sát giao diện hiện tại; xác nhận đúng project và trạng thái đăng nhập.
3. Chuyển sang Video → Thành phần.
4. Gắn đúng avatar/nhân vật theo alias; gắn ảnh hoặc video bối cảnh mà người dùng chỉ định.
5. Mở cài đặt và xác minh Omni 1.1 Flash, 9:16, chất lượng cao nhất, 10 giây, x1.
6. Chuyển brief thành mini-story 10 giây: thiết lập → phát triển → cao trào → living finish.
7. Viết 2–3 cảnh có mốc thời gian, ống kính, chuyển động máy, hành động, điểm nhìn, biểu cảm và trạng thái đầu/cuối rõ ràng.
8. Thêm khóa nhận diện, bối cảnh, giải phẫu, hành động liên tục, không thoại và các lỗi cần tránh.
9. Kiểm tra prompt theo chính sách rồi bấm tạo.
10. Chờ hoàn tất; không để người dùng thiếu cập nhật quá lâu.
11. Mở video, phát trọn 10 giây và kiểm tra các mốc 0–2s, 4–6s, 8–10s.
12. Nếu có lỗi rõ như đổi người, sai bối cảnh, đổi tư thế, đứng hình sớm hoặc chỉ có một góc máy: dùng lại câu lệnh, sửa đúng nguyên nhân và tạo lại tối đa một lần.
13. Khi đạt, bật video cho người dùng xem. Chỉ tải file nếu được yêu cầu.

## Cổng chất lượng đầu ra

- Đúng nhân vật/component; avatar không đổi người hoặc trang phục.
- Đúng bối cảnh đã chọn và bối cảnh hiện rõ, không chỉ “gần giống”.
- Có đúng 2–3 góc quay có chủ đích, ưu tiên cận cảm xúc; máy quay chuyển động mềm và điện ảnh.
- Ánh mắt và biểu cảm phát triển theo chuỗi; không có khuôn mặt trống hoặc nụ cười đóng băng.
- Hành động là một câu chuyện liên tục. Với cảnh bế, cô gái phải được bế ở đầu, giữa và cuối; chỉ máy quay được đổi vị trí.
- Không dừng từ giây 8. Hành động tiếp tục ít nhất tới giây 9,2 và kết bằng living finish có nhịp thở, chớp mắt, tóc/vải và camera drift nhẹ.
- Không thoại, không voice-over, không chữ/logo tự sinh.
- Độ nét cảm nhận đạt yêu cầu: mắt, mặt, tóc và vải rõ; không haze, soft focus hoặc motion blur trên mặt.

## Giới hạn tự động

- Không tự đăng nhập, nhập mật khẩu, OTP hoặc lưu bí mật.
- Không xóa tài sản, đổi tên/chia sẻ project, mua credit hoặc tạo nhiều hơn x1 nếu chưa được yêu cầu.
- Không tải xuống nếu người dùng chưa yêu cầu.
- Không gọi bản lỗi là hoàn thành; báo trung thực giới hạn của Flow nếu lần sửa vẫn không đạt.
