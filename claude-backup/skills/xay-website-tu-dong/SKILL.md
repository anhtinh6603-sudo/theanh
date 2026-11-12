---
name: xay-website-tu-dong
description: Xây dựng website tự động cho doanh nghiệp/thương hiệu/dịch vụ nhiều trang - từ mục tiêu và sơ đồ trang, chọn nền tảng (WordPress, no-code hoặc code trên Vercel/Netlify), viết nội dung, SEO cơ bản cho tiếng Việt, đến các phần tự động (form liên hệ, đặt lịch, thông báo, quy trình đăng bài blog có duyệt, sao lưu, theo dõi Google Analytics/Search Console). Dùng skill này khi người dùng muốn làm website, web giới thiệu công ty, web khách sạn/nhà hàng/dịch vụ, blog, tối ưu SEO, hoặc "website tự chạy" - kể cả khi họ chỉ nói "làm cho tôi cái web". Nếu chỉ cần một trang bán một sản phẩm thì dùng skill xay-trang-ban-hang-tu-dong.
---

# Xây website tự động

Website giới thiệu doanh nghiệp/thương hiệu khác trang bán hàng ở chỗ: nhiều trang, cần được tìm thấy (SEO), và cần **dễ cập nhật** mà không phụ thuộc mãi vào người làm web. "Tự động" ở đây là: nhận liên hệ/đặt lịch, thông báo, đăng nội dung theo quy trình có duyệt, sao lưu và theo dõi số liệu.

## Bước 0 - Hỏi nhanh (gộp, tối đa 6 câu)

1. Doanh nghiệp làm gì, khách là ai, khách cần tìm thấy điều gì đầu tiên?
2. Mục tiêu chính của web: nhận liên hệ/đặt lịch/đặt phòng, bán hàng, tạo uy tín, hay thu hút qua tìm kiếm?
3. Đã có tên miền, hosting, logo, ảnh thật, nội dung sẵn chưa?
4. Ai sẽ cập nhật nội dung sau này và họ rành kỹ thuật đến đâu?
5. Ngân sách hằng tháng chấp nhận được; cần tiếng Việt hay đa ngôn ngữ?
6. Web tham khảo yêu thích (nếu có).

## Bước 1 - Sơ đồ trang và luồng khách

Lập sơ đồ trang (thường: Trang chủ, Giới thiệu, Dịch vụ/Sản phẩm, Bảng giá hoặc Liên hệ báo giá, Bài viết/Kiến thức, Câu hỏi thường gặp, Liên hệ). Với mỗi trang ghi: mục đích, từ khóa chính, một hành động mong muốn. Mọi trang phải dẫn được đến **một** cách liên hệ hoặc đặt lịch.

## Bước 2 - Chọn nền tảng

| Hướng | Hợp khi | Lưu ý |
|---|---|---|
| WordPress (hoặc trình dựng web có sẵn) | Người cập nhật không rành code, cần plugin sẵn | Phải cập nhật và bảo mật thường xuyên |
| Trang tĩnh/Next.js đặt trên Vercel hoặc Netlify | Cần nhanh, rẻ, gọn; có người biết chút kỹ thuật | Cần cách quản lý nội dung |
| Trang tĩnh + Notion/Google Sheets làm nơi soạn nội dung | Muốn sửa nội dung như sửa tài liệu | Cần bước đồng bộ nội dung sang web |

Mặc định: người không rành kỹ thuật → hướng đầu; người muốn gọn, nhanh → hướng hai hoặc ba. Nói rõ ưu nhược điểm rồi để người dùng chọn. Nếu người dùng đã kết nối Vercel hoặc Notion, đề xuất dùng. **Tên miền và hosting phải đứng tên người dùng**, không để nhà cung cấp giữ quyền sở hữu.

## Bước 3 - Nội dung và thiết kế

- Viết nội dung từng trang hoàn chỉnh bằng tiếng Việt, đúng giọng thương hiệu, câu ngắn, dễ quét mắt (tiêu đề rõ, đoạn ngắn).
- Dùng thông tin và ảnh thật của người dùng. Không bịa chứng nhận, giải thưởng, khách hàng, đánh giá, số liệu.
- Thiết kế ưu tiên điện thoại; tốc độ tải nhanh (nén ảnh, không nhúng thừa); chữ đủ lớn, độ tương phản tốt, có mô tả cho ảnh.
- Nếu tạo mã: một cấu trúc thư mục rõ ràng, README bằng tiếng Việt (cách chạy, cách sửa nội dung, cách đưa lên mạng).

## Bước 4 - SEO cơ bản (cho tìm kiếm tiếng Việt)

Mỗi trang: một tiêu đề (title) và mô tả (meta description) riêng có từ khóa chính, một thẻ H1, đường dẫn (URL) ngắn dễ đọc, ảnh có mô tả, liên kết nội bộ giữa các trang. Toàn site: sơ đồ trang (sitemap), robots, HTTPS, dữ liệu có cấu trúc phù hợp (thông tin doanh nghiệp, câu hỏi thường gặp), tốc độ ổn trên điện thoại. Với doanh nghiệp địa phương: hồ sơ Google Business, địa chỉ/số điện thoại nhất quán. Chỉ nói xu hướng từ khóa bằng số liệu khi đã tra cứu thật; nếu chưa, ghi rõ là ước đoán.

## Bước 5 - Các phần tự động

1. **Form liên hệ/đặt lịch** → lưu vào bảng (Google Sheets/Notion) → thông báo cho chủ (email/Zalo/Telegram) → email xác nhận cho khách.
2. **Đặt lịch/đặt phòng**: dùng công cụ đặt lịch hoặc form + bảng; tránh trùng lịch.
3. **Đăng bài blog theo quy trình**: ý tưởng → bản nháp (AI hỗ trợ) → **người kiểm tra/sửa/duyệt** → đăng → chia sẻ lên kênh. Nội dung do AI viết luôn cần người duyệt và kiểm chứng số liệu trước khi đăng; không đăng thẳng tự động.
4. **Theo dõi**: Google Analytics 4 và Search Console; báo cáo tóm tắt hằng tháng.
5. **Sao lưu và giám sát**: sao lưu định kỳ, báo khi web ngừng hoạt động, nhắc gia hạn tên miền/chứng chỉ.

Không tạo hay bật quy trình chạy thật khi chưa được xác nhận. Không nhờ dán mật khẩu, khóa API vào chat: hướng dẫn cấp quyền bằng vai trò/lời mời hoặc nhập vào biến môi trường.

## Bảo mật và pháp lý

Có chính sách bảo mật và thông báo khi thu dữ liệu cá nhân (tên, số điện thoại, email); xin đồng ý khi gửi tin quảng bá; không thu thông tin không cần thiết. Hạn chế plugin/mã bên thứ ba không rõ nguồn; cập nhật thường xuyên; dùng mật khẩu mạnh và xác thực hai bước cho tài khoản quản trị.

## Bàn giao và kiểm tra cuối

Giao: sơ đồ trang, nội dung từng trang, mã/cấu hình hoặc hướng dẫn dựng, luồng tự động, checklist SEO, hướng dẫn cập nhật cho người phụ trách. Trước khi mở web: thử form thật, xem trên điện thoại, kiểm tra tốc độ, link gãy, tiêu đề/mô tả từng trang, và mọi thông tin liên hệ chính xác.
