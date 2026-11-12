---
name: xay-app-phan-mem-tu-dong
description: Xây dựng ứng dụng/phần mềm nhỏ tự động hóa công việc (quản lý đơn, khách, kho, đặt phòng, chấm công, báo cáo, công cụ nội bộ) - từ xác định vấn đề, thu hẹp phạm vi MVP, chọn hướng no-code hay tự viết mã, mô hình dữ liệu, màn hình, đến viết mã chạy được, kiểm thử, triển khai và bảo trì. Dùng skill này khi người dùng muốn làm app, phần mềm, công cụ nội bộ, hệ thống quản lý, bot chạy nền, tự động hóa bằng code, hoặc nói "tôi muốn có phần mềm làm việc này" - kể cả khi họ không biết lập trình.
---

# Xây app/phần mềm tự động

Phần lớn ứng dụng thất bại vì làm quá to ngay từ đầu. Cách làm ở đây: **giải quyết một việc thật, bằng phiên bản nhỏ nhất dùng được (MVP), rồi mở rộng**. Người dùng có thể không biết lập trình: nói bằng lời thường, mỗi lần chỉ giao một phần chạy được.

## Bước 0 - Hỏi nhanh (gộp, tối đa 6 câu)

1. Việc gì đang tốn thời gian/dễ sai nhất? Hiện đang làm thế nào (Excel, sổ giấy, Zalo)?
2. Ai dùng (một mình, nhân viên, khách) và trên thiết bị nào (điện thoại, máy tính)?
3. Dữ liệu chính gồm những gì (khách, đơn, phòng, sản phẩm...) và đang lưu ở đâu?
4. Việc nào phải tự động (nhắc việc, gửi tin, tạo báo cáo, đồng bộ)?
5. Có dữ liệu nhạy cảm không (thông tin cá nhân, thanh toán)?
6. Mức kỹ thuật, ngân sách, và ai sẽ bảo trì sau này?

## Bước 1 - Thu hẹp thành MVP

Viết **một trang đặc tả**: vấn đề, người dùng, 3-5 tình huống sử dụng quan trọng nhất ("Nhân viên nhập đơn trong dưới 30 giây"), những thứ **chưa làm** ở phiên bản đầu, và cách biết thành công (đo được). Phần vượt quá 5 tình huống chuyển sang "giai đoạn sau". Người dùng thường muốn nhiều hơn: giúp họ chọn, đừng ôm hết.

## Bước 2 - Chọn hướng làm

| Hướng | Hợp khi |
|---|---|
| Bảng tính + tự động (Google Sheets + Apps Script, Airtable, Notion, Make/n8n) | Quy trình đơn giản, ít người dùng, cần chạy ngay |
| No-code/low-code làm app (AppSheet, Glide, Softr...) | Cần giao diện điện thoại, không muốn viết mã |
| Tự viết mã (web app: giao diện + máy chủ + cơ sở dữ liệu) | Cần logic riêng, nhiều người dùng, muốn làm chủ hoàn toàn |
| Script chạy nền (Python/Node) | Việc lặp lại không cần giao diện: kéo dữ liệu, gửi báo cáo, xử lý file |

Luôn đề xuất hướng **đơn giản nhất còn đáp ứng được**; nêu chi phí và giới hạn (số người dùng, dữ liệu, phụ thuộc nhà cung cấp). Giá/tính năng nền tảng thay đổi: kiểm tra tài liệu hiện hành nếu có công cụ tìm web.

## Bước 3 - Thiết kế trước khi viết mã

- **Mô hình dữ liệu**: liệt kê các bảng/đối tượng, trường, quan hệ; cho ví dụ dữ liệu thật.
- **Màn hình và luồng**: danh sách màn hình, ai thấy gì, thao tác chính.
- **Phân quyền**: ai được xem/sửa/xóa gì.
- **Tự động**: sự kiện nào kích hoạt việc gì, ai được thông báo.

Cho người dùng xem và xác nhận thiết kế (bằng văn bản hoặc bản phác giao diện đơn giản) **trước** khi viết nhiều mã.

## Bước 4 - Viết mã theo lát cắt dọc

Làm từng lát nhỏ chạy được từ đầu đến cuối (ví dụ: nhập một đơn → lưu → hiện trong danh sách) thay vì làm toàn bộ giao diện rồi mới nối dữ liệu. Sau mỗi lát:
- **Chạy thử thật** khi có môi trường (chạy mã, kiểm tra đầu ra) rồi mới nói "xong"; nếu không chạy được thì nói rõ chưa kiểm chứng.
- Ghi chú cách chạy và cách kiểm tra.

Chuẩn mã: tên rõ nghĩa, tách cấu hình khỏi mã, xử lý lỗi thân thiện, ghi nhật ký (log) cho phần tự động.

## Bước 5 - Bảo mật (không bỏ qua)

- Bí mật (khóa API, mật khẩu cơ sở dữ liệu) để trong biến môi trường, không viết vào mã, không dán vào chat.
- Kiểm tra và làm sạch dữ liệu nhập vào; đăng nhập và phân quyền phía máy chủ; không lưu mật khẩu dạng thô.
- Chỉ lưu dữ liệu cá nhân thật cần thiết; có sao lưu định kỳ; có cách xóa dữ liệu theo yêu cầu.
- Không đưa mã có khóa thật lên nơi công khai.

## Bước 6 - Triển khai và bảo trì

Giao bản README tiếng Việt: app làm gì, cách cài/chạy, biến môi trường cần có, cách cập nhật, cách sao lưu, cách xử lý lỗi thường gặp. Hướng dẫn triển khai (Vercel/Netlify cho web, dịch vụ chạy nền cho script; dùng connector Vercel nếu người dùng đã kết nối và đồng ý). Chốt ai bảo trì và lịch xem lại. Ghi nhật ký thay đổi cho mỗi phiên bản.

## Định dạng bàn giao

Mỗi lần giao: (1) mã hoặc file chạy được, (2) cách thử trong 3 bước, (3) danh sách việc chưa làm/rủi ro đã biết, (4) bước tiếp theo đề xuất. Nếu công việc quá lớn cho một lượt, chia thành giai đoạn và nói rõ giai đoạn hiện tại.

## Kiểm tra cuối

MVP có giải quyết đúng việc đã chọn? Đã chạy thử với dữ liệu giống thật? Không còn bí mật nằm trong mã? Người dùng biết cách chạy, sửa và sao lưu mà không cần hỏi lại?
