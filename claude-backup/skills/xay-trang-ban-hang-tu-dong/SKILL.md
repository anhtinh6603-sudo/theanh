---
name: xay-trang-ban-hang-tu-dong
description: Xây dựng trang bán hàng (landing page/sales page) tự động - từ ưu đãi, cấu trúc trang, nội dung thuyết phục, form đặt hàng, thanh toán/COD/chuyển khoản QR, đến luồng tự động sau khi có đơn (ghi vào bảng tính, báo về Zalo/email, xác nhận cho khách) và đo lường Pixel/GA4. Dùng skill này khi người dùng muốn làm trang bán hàng, landing page, trang đặt hàng, funnel bán sản phẩm/khóa học/dịch vụ, "trang tự nhận đơn", hoặc cần tạo và đưa trang bán hàng lên mạng - kể cả khi họ chỉ nói "làm cho tôi cái trang để bán hàng".
---

# Xây trang bán hàng tự động

Một trang bán hàng tốt làm **một việc**: dẫn người xem đến một hành động (đặt hàng, đăng ký, đặt lịch). "Tự động" nghĩa là sau khi khách bấm, mọi thứ còn lại (ghi đơn, báo cho chủ, xác nhận cho khách, theo dõi) chạy không cần ai bấm tay.

## Bước 0 - Hỏi nhanh (gộp, tối đa 5 câu)

1. Bán gì, giá bao nhiêu, ai mua (mô tả một khách điển hình)?
2. Hành động mong muốn: đặt hàng COD, chuyển khoản, đăng ký để được gọi lại, hay đặt lịch?
3. Có gì để làm bằng chứng thật: ảnh sản phẩm, đánh giá thật, số liệu thật, cam kết đổi trả?
4. Khách sẽ đến từ đâu (quảng cáo Facebook/TikTok, Zalo, tìm kiếm)?
5. Người dùng muốn thứ gì: file trang để tự đưa lên mạng, hay Claude xuất bản luôn (nếu có công cụ)?

## Bước 1 - Chốt ưu đãi (offer) trước khi làm trang

Viết một câu: *Ai* nhận *kết quả gì*, trong *bao lâu*, với *giá nào*, và *vì sao tin được*. Nếu người dùng chưa rõ, giúp họ chốt trước. Trang đẹp không cứu được ưu đãi mờ nhạt.

## Bước 2 - Cấu trúc trang (mặc định, có thể điều chỉnh theo sản phẩm)

1. **Đầu trang**: lời hứa chính bằng ngôn ngữ khách hay dùng + ảnh/video sản phẩm + nút hành động.
2. **Vấn đề**: mô tả đúng nỗi đau, không phóng đại.
3. **Giải pháp**: sản phẩm giải quyết thế nào, 3-5 lợi ích (lợi ích trước, tính năng sau).
4. **Bằng chứng**: đánh giá/ảnh/số liệu **thật**. Chưa có thì để trống mục này hoặc dùng cam kết rõ ràng, tuyệt đối không bịa.
5. **Giá và gói**: rõ ràng, có phí ship, thời gian giao.
6. **Chính sách**: đổi trả, bảo hành, thanh toán.
7. **Câu hỏi thường gặp**: 5-8 câu, gỡ đúng các băn khoăn trước khi mua.
8. **Form đặt hàng**: ít trường nhất có thể (tên, số điện thoại, địa chỉ, số lượng). Nút bấm nêu rõ điều sẽ xảy ra ("Đặt hàng - thanh toán khi nhận").
9. **Chân trang**: thông tin doanh nghiệp, liên hệ, chính sách bảo mật.

Trang phải dùng tốt trên điện thoại trước (phần lớn khách đến từ điện thoại): chữ đủ lớn, nút dễ bấm, tải nhanh, ảnh nén.

## Bước 3 - Tự động sau khi có đơn

Vẽ luồng: **Form → lưu đơn (Google Sheets/Notion/CRM) → báo cho chủ (Zalo/Telegram/email) → xác nhận cho khách → theo dõi trạng thái**. Gợi ý cách làm theo mức độ:

- **Đơn giản**: form gửi vào Google Sheets + email thông báo (Apps Script hoặc dịch vụ form).
- **Trung bình**: form → webhook Make/n8n → ghi bảng, gửi thông báo, gửi email xác nhận.
- **Có thanh toán online**: chuyển khoản QR (VietQR) kèm mã đơn duy nhất + dịch vụ đối soát tự động (như payOS, SePay, Casso - kiểm tra điều kiện và phí hiện hành), hoặc cổng thanh toán. Xác thực chữ ký webhook; không đặt khóa bí mật trong mã chạy trên trình duyệt.

Nếu người dùng đã kết nối Make, Notion, Google Drive hoặc Vercel, đề xuất dùng chúng; không tạo/bật gì chạy thật khi chưa được xác nhận.

## Bước 4 - Làm ra trang

Tạo **một file HTML tự chứa** (CSS/JS gộp trong file, ảnh nhúng hoặc đường dẫn thật), tiếng Việt, đặt sẵn chỗ cho mã theo dõi. Nếu môi trường có công cụ xuất bản (Artifact, connector Vercel) và người dùng đồng ý thì xuất bản; nếu không, hướng dẫn từng bước đưa lên hosting/Vercel/Netlify và trỏ tên miền. Tên miền và hosting phải đứng tên người dùng.

Ghi chú cho trang xuất bản: dùng lưu trữ trình duyệt chỉ cho tiện ích nhỏ; đơn hàng phải đi qua dịch vụ nhận dữ liệu thật, không lưu ở trình duyệt.

## Bước 5 - Đo lường

Cài Meta Pixel/TikTok Pixel và GA4 với các sự kiện: xem trang, bắt đầu điền form, gửi đơn. Gắn UTM cho từng nguồn quảng cáo. Chỉ số cần theo dõi: tỷ lệ chuyển đổi, chi phí mỗi đơn, tỷ lệ đơn hủy/không nghe máy.

## Rào chắn trung thực và pháp lý

- **Không bịa** đánh giá, ảnh khách hàng, con số "đã bán", đồng hồ đếm ngược giả, "chỉ còn X suất" giả, hoặc chứng nhận không có.
- Không hứa kết quả chắc chắn; với sản phẩm sức khỏe, tài chính, làm đẹp: tránh tuyên bố chữa bệnh/cam kết lợi nhuận.
- Có chính sách đổi trả, chính sách bảo mật, và thông báo khi thu dữ liệu cá nhân. Không thu số thẻ trên form tự làm.
- Hướng dẫn thử đặt một đơn thật từ điện thoại trước khi chạy quảng cáo.

## Kiểm tra cuối

Một khách lạ đọc 5 giây có hiểu bán gì, cho ai, giá bao nhiêu? Nút hành động thấy được trên màn hình điện thoại ngay từ đầu? Đơn thử đã chạy hết luồng tự động? Đã kiểm tra mọi claim đều có căn cứ?
