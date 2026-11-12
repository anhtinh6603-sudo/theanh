---
name: xay-quy-trinh-email-tu-dong
description: Xây dựng quy trình email marketing tự động (email chào mừng, nuôi dưỡng khách, giỏ hàng bỏ quên, sau mua, kéo khách cũ, bản tin định kỳ) - gồm sơ đồ chuỗi email, viết đủ nội dung từng email, phân nhóm khách, kiểm thử tiêu đề, thiết lập gửi (SPF/DKIM/DMARC), quy tắc hủy đăng ký và tuân thủ. Dùng skill này khi người dùng muốn làm email marketing, chuỗi email tự động, newsletter, autoresponder, nuôi khách hàng bằng email, Mailchimp/Brevo/MailerLite/Klaviyo, hoặc soạn nhiều email liên hoàn - kể cả khi họ chỉ nói "muốn gửi email cho khách tự động".
---

# Xây quy trình email tự động

Email tự động tốt giống một người bán hàng kiên nhẫn: đúng lúc, đúng người, mỗi email chỉ một việc, và biết dừng khi khách đã mua hoặc không muốn nhận nữa.

## Bước 0 - Hỏi nhanh (gộp, tối đa 5 câu)

1. Bán gì, khách là ai; khách mua một lần hay mua lặp lại?
2. Danh sách email từ đâu ra (form trên web, mua hàng, sự kiện)? Khách đã đồng ý nhận chưa?
3. Mục tiêu: chào mừng khách mới, chốt đơn, kéo giỏ hàng, sau mua, hay giữ liên lạc?
4. Đang dùng công cụ gì (Mailchimp, Brevo, MailerLite, Klaviyo, Google Workspace) và có tên miền riêng chưa?
5. Số lượng danh sách, tần suất mong muốn, giọng thương hiệu.

## Bước 1 - Chọn chuỗi cần xây (thường bắt đầu từ 1-2 chuỗi)

| Chuỗi | Kích hoạt | Số email gợi ý |
|---|---|---|
| Chào mừng | Khách đăng ký/để lại email | 3-5 trong 7-10 ngày |
| Nuôi dưỡng | Khách chưa mua | 4-6, thưa dần |
| Giỏ hàng bỏ quên | Thêm giỏ nhưng chưa thanh toán | 2-3 trong vài ngày |
| Sau mua | Đã mua | 3-4: cảm ơn, hướng dẫn dùng, xin phản hồi, gợi ý mua thêm |
| Kéo khách cũ | Lâu không tương tác | 2-3, có lối thoát rõ |
| Bản tin | Định kỳ | Theo lịch cố định |

## Bước 2 - Sơ đồ chuỗi (sản phẩm bàn giao)

Với mỗi chuỗi lập bảng: **email số - điều kiện kích hoạt - độ trễ - mục đích - tiêu đề - đoạn xem trước - nút hành động - điều kiện dừng/thoát**. Điều kiện dừng bắt buộc: khách đã mua, đã trả lời, hoặc đã hủy đăng ký thì thoát chuỗi.

## Bước 3 - Viết đủ nội dung từng email

Viết sẵn toàn bộ, không để khung trống. Mỗi email:
- **Tiêu đề** ngắn, rõ lợi ích hoặc lý do mở; đưa 2-3 phương án cho phần thử nghiệm A/B.
- **Đoạn xem trước** bổ sung cho tiêu đề, không lặp lại.
- **Nội dung**: 80-200 chữ, một ý chính, một nút hành động, đọc được trên điện thoại. Câu ngắn, xưng hô nhất quán với thương hiệu.
- **Chân email**: tên/địa chỉ đơn vị gửi, lý do khách nhận email, đường dẫn hủy đăng ký.
- Cá nhân hóa hợp lý (tên, sản phẩm đã xem). Chỉ nói giá, ưu đãi, thời hạn có thật; **không bịa khan hiếm hay đánh giá**.

## Bước 4 - Phân nhóm

Đề xuất vài nhóm đơn giản và đủ dùng: khách mới, đã mua, mua nhiều lần, lâu không tương tác, quan tâm sản phẩm X. Mỗi nhóm có quy tắc vào/ra rõ ràng. Không tạo quá nhiều nhóm khi danh sách còn nhỏ.

## Bước 5 - Thiết lập kỹ thuật để email vào hộp thư chính

- Dùng tên miền riêng của doanh nghiệp để gửi; thiết lập **SPF, DKIM, DMARC** cho tên miền (nêu từng bước theo nhà cung cấp tên miền/công cụ email của người dùng).
- Tài khoản Gmail/Google cá nhân **không** dùng để gửi hàng loạt; dùng công cụ email marketing.
- Có liên kết hủy đăng ký dễ thấy, hủy được trong một bước; xử lý yêu cầu hủy ngay.
- Làm sạch danh sách: bỏ địa chỉ trả lại (bounce), người không mở trong thời gian dài; giữ tỷ lệ khiếu nại spam rất thấp. Với danh sách mới hoặc tên miền mới, tăng khối lượng gửi dần.
- Yêu cầu của các hộp thư lớn về xác thực và hủy đăng ký đang được siết: kiểm tra hướng dẫn hiện hành của nhà cung cấp.

## Bước 6 - Tuân thủ

- **Chỉ gửi cho người đã đồng ý** (đăng ký, mua hàng và có thông báo rõ). Không mua danh sách email, không cạo email từ web.
- Tuân thủ quy định chống thư rác và bảo vệ dữ liệu cá nhân của Việt Nam (kiểm tra văn bản hiện hành); nếu có khách nước ngoài, cân nhắc thêm quy định nơi họ ở (như GDPR, CAN-SPAM).
- Lưu lại bằng chứng đồng ý (thời điểm, nguồn đăng ký).

## Bước 7 - Kiểm thử và đo lường

Gửi thử cho chính người dùng và 2-3 tài khoản khác (Gmail, Outlook); xem trên điện thoại; kiểm tra mọi liên kết, nút hủy, biến cá nhân hóa (không hiện "Xin chào {tên}" trần). Theo dõi: tỷ lệ mở (chỉ mang tính tham khảo), tỷ lệ bấm, tỷ lệ chuyển đổi, tỷ lệ hủy đăng ký, tỷ lệ khiếu nại. Mỗi lần chỉ thử một biến (tiêu đề hoặc nút hành động), đủ lượng gửi rồi mới kết luận.

## Rào chắn khi dùng công cụ

Nếu người dùng đã kết nối Gmail hoặc công cụ khác, chỉ **tạo bản nháp**; gửi thật cần người dùng xác nhận rõ ràng từng lần, và không dùng để gửi hàng loạt. Không nhờ dán mật khẩu/khóa API vào chat. Không bật chuỗi tự động chạy thật khi chưa qua bước kiểm thử.

## Kiểm tra cuối

Mỗi chuỗi có điều kiện dừng? Mọi email có lối hủy đăng ký? Danh sách có bằng chứng đồng ý? SPF/DKIM/DMARC đã cài? Mọi con số, ưu đãi trong email có thật?
