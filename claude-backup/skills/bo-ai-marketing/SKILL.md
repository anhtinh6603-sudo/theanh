---
name: bo-ai-marketing
description: Bộ AI Marketing bán hàng gồm 10 mô-đun - Nghiên cứu thị trường, Content, Thiết kế, Video, Fanpage Chatbot, Zalo CSKH, Website và Landing Page, Quảng cáo, Email Marketing, Báo cáo. Dùng skill này để điều phối cả hệ thống, khi người dùng muốn xây hệ thống marketing tự động, hỏi "bắt đầu từ đâu", muốn lộ trình bán hàng bằng AI, nhắc tới "bộ AI" hoặc tên một mô-đun, muốn biết mô-đun nào làm được gì và cần thêm công cụ gì, hoặc muốn nối nhiều khâu (nghiên cứu, nội dung, trang bán hàng, quảng cáo, chăm sóc khách, báo cáo) thành một quy trình.
---

# Bộ AI Marketing bán hàng

Bộ này gồm 10 mô-đun, mỗi mô-đun do một skill riêng đảm nhiệm. Skill này là **bản đồ và người điều phối**: chọn đúng mô-đun, giữ thông tin chung nhất quán giữa các mô-đun, và nói thật mô-đun nào Claude làm trọn được, mô-đun nào cần công cụ hoặc tài khoản bên ngoài.

## Bản đồ mô-đun

| Mô-đun | Việc chính | Skill phụ trách |
|---|---|---|
| 1. AI Nghiên cứu thị trường | Tìm nhu cầu, đối thủ, khách mục tiêu, sản phẩm đang được quan tâm | `ai-nghien-cuu-thi-truong` |
| 2. AI Content | Bài Facebook, kịch bản video, email, tin nhắn chăm sóc | `huong-dan-y-tuong-nghien-cuu-viet-content` (bài, kịch bản, lịch); `xay-quy-trinh-email-tu-dong` (email); `zalo-tra-loi-khach` (tin nhắn khách) |
| 3. AI Thiết kế | Ảnh quảng cáo, poster, thumbnail, banner, hình sản phẩm | `ai-thiet-ke-quang-cao` |
| 4. AI Video | Kịch bản, tạo video AI, lồng tiếng, phụ đề, cắt video ngắn | `huong-dan-lam-video-bang-ai`, `huong-dan-edit-video-bang-ai` (và các skill dựng video khác của người dùng nếu đã cài) |
| 5. AI Fanpage Chatbot | Trả lời bình luận/inbox, tư vấn, thu thông tin khách | `xay-fanpage-chatbot-tu-dong` |
| 6. AI Zalo CSKH | Phân loại khách, tin chăm sóc, nhắc lịch, sau bán | `xay-zalo-cham-soc-khach-tu-dong` |
| 7. AI Website và Landing Page | Website, trang bán hàng, form thu lead, trang thanh toán | `xay-website-tu-dong`, `xay-trang-ban-hang-tu-dong` |
| 8. AI Quảng cáo | Nội dung quảng cáo, chia nhóm khách, theo dõi chỉ số, đề xuất tối ưu | `xay-chay-quang-cao-tu-dong` |
| 9. AI Email Marketing | Chuỗi chào mừng, tư vấn, bán hàng, sau mua | `xay-quy-trinh-email-tu-dong` |
| 10. AI Báo cáo | Doanh thu, số khách, chi phí quảng cáo, hiệu quả từng kênh | `ai-bao-cao-kinh-doanh` |

Khi người dùng nêu một việc thuộc mô-đun nào, **đọc SKILL.md của skill phụ trách rồi làm theo nó**. Skill nào chưa cài thì nói rõ và làm theo tinh thần của mô-đun (nhưng báo người dùng skill đó chưa có).

## Lộ trình gợi ý (thứ tự làm để đỡ tốn tiền)

1. **Nghiên cứu (1) →** chốt sản phẩm, khách mục tiêu, ưu đãi. Chưa chốt được thì đừng làm các bước sau.
2. **Nơi nhận khách (7) →** trang bán hàng/website + cách đo lường (Pixel/GA4). Chưa có nơi nhận thì đừng chạy quảng cáo.
3. **Nội dung và hình ảnh (2, 3, 4) →** bộ bài đăng, ảnh, video ngắn xoay quanh cùng một thông điệp.
4. **Quảng cáo thử nhỏ (8) →** sau khi đã có trang và đo lường; đặt trần chi tiêu và tiêu chí dừng.
5. **Xử lý khách đến (5, 6) →** chatbot fanpage, Zalo: chỉ dựng khi đã có khách đến đều.
6. **Nuôi và bán lại (9) →** email chào mừng, sau mua, kéo khách cũ.
7. **Vòng lặp hằng tuần (10 → 1, 2, 3, 8) →** báo cáo cho thấy chỗ nào hụt, quay lại sửa đúng khâu đó.

Không bắt buộc làm đủ 10 mô-đun: hỏi người dùng đang ở giai đoạn nào và ngân sách/thời gian ra sao rồi đề xuất **1-3 mô-đun** làm trước.

## Hồ sơ dự án chung (hỏi một lần, dùng lại cho mọi mô-đun)

Ghi ngắn và xác nhận với người dùng khi bắt đầu; các mô-đun sau dùng lại, không hỏi lại:
- **Sản phẩm/dịch vụ** và **giá** (chỉ số chắc chắn).
- **Khách mục tiêu** (1-2 câu) và **nỗi đau chính**.
- **Ưu đãi/thông điệp chính** (một câu).
- **Giọng thương hiệu** và cách xưng hô; màu sắc/logo nếu có.
- **Kênh đang có** (fanpage, Zalo/OA, website, email, tài khoản quảng cáo).
- **Con số kinh tế**: giá vốn, ROAS hòa vốn, CPA mục tiêu (nếu đã tính).
- **Giới hạn**: ngân sách thử, người trực, khu vực, điều không được nói.

Đề nghị lưu hồ sơ này thành một tài liệu để lần sau dán lại là dùng được ngay.

## Nói thật về "tự động"

Claude soạn nội dung, thiết kế quy trình, viết mã, dựng trang, tổng hợp số liệu **khi được gọi trong cuộc trò chuyện**. Để chạy **liên tục 24/7** (trả lời inbox, gửi tin theo lịch, kéo số hằng ngày) cần công cụ bên ngoài: nền tảng chatbot, Zalo OA, công cụ email marketing, Make/n8n hoặc máy chủ. Chi tiết mức khả thi từng mô-đun ở `references/tinh-kha-thi.md`: đọc khi người dùng hỏi "làm được đến đâu", "cần gì thêm", hoặc trước khi hứa một tính năng tự động.

## Nguyên tắc chung cho mọi mô-đun

- **Không bịa**: giá, ưu đãi, đánh giá, số liệu, kết quả, chứng nhận. Thiếu dữ liệu thì hỏi hoặc ghi "cần bổ sung".
- **Không tự chi tiền, gửi hàng loạt, đăng bài công khai, hay bật tự động** khi chưa được người dùng xác nhận rõ từng thao tác.
- **Chỉ nhắn/gửi cho người đã đồng ý**; có lối từ chối; tuân thủ quy định chống tin nhắn rác và bảo vệ dữ liệu cá nhân của Việt Nam (kiểm tra văn bản hiện hành).
- **Không nhờ dán mật khẩu, mã OTP, token, khóa API vào chat.** Hướng dẫn nhập trực tiếp vào công cụ hoặc dùng vai trò/lời mời.
- **Khách hỏi có phải AI không thì trả lời thật.** Nội dung AI trông như thật thì gắn nhãn theo yêu cầu nền tảng.
- Chính sách, giá, giới hạn của nền tảng thay đổi: kiểm tra tài liệu chính thức khi có công cụ tìm web, và nói rõ thông tin nào có thể đã cũ.

## Kiểm tra cuối mỗi lần điều phối

Đã xác định đúng giai đoạn và chỉ đề xuất số mô-đun vừa sức? Đã dùng đúng skill phụ trách? Thông tin trong hồ sơ dự án nhất quán giữa các mô-đun? Đã nói rõ phần nào Claude làm trọn, phần nào cần công cụ ngoài?
