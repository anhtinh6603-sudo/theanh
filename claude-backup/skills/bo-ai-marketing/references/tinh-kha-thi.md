# Mức khả thi từng mô-đun

Đánh giá dựa trên kiểm tra thực tế môi trường Claude (ngày 19/09/2026): thư viện Python (Pillow, pandas, openpyxl, matplotlib), ffmpeg, LibreOffice có sẵn; mạng ra ngoài từ môi trường chạy mã **bị chặn** với Google Trends, Facebook Ad Library và dịch vụ giọng đọc (đã thử, bị từ chối); connector Canva đã cài nhưng cần kết nối lại; connector đọc số liệu quảng cáo (Supermetrics, Windsor.ai) tồn tại nhưng là dịch vụ bên thứ ba chưa cài. Môi trường và chính sách nền tảng thay đổi: kiểm tra lại khi cần.

Ký hiệu: **Cao** = Claude làm trọn trong cuộc trò chuyện; **Trung bình** = Claude làm phần lớn, phần còn lại cần công cụ/tài khoản ngoài; **Thấp** = chủ yếu là thiết kế và hướng dẫn.

| Mô-đun | Mức | Claude làm trọn | Cần thêm bên ngoài | Giới hạn thật |
|---|---|---|---|---|
| 1. Nghiên cứu thị trường | Cao (phân tích), Trung bình (dữ liệu thực) | Tìm web công khai, so sánh đối thủ, dựng persona, chấm điểm cơ hội, viết báo cáo có nguồn | Tùy chọn: công cụ dữ liệu trả phí; người dùng mở Google Trends/Ad Library/sàn rồi dán hoặc chụp | Không có doanh số thật của đối thủ/sàn; nhiều nguồn chặn truy cập tự động |
| 2. Content | Cao | Bài Facebook, kịch bản video, email, tin nhắn, lịch 30 ngày | - | Không tự đăng bài; cần người duyệt và kiểm chứng số liệu |
| 3. Thiết kế | Cao (banner/thumbnail/story chữ + nền), Thấp (ảnh chụp thực tế tạo mới) | Xuất PNG đúng kích thước với chữ tiếng Việt chuẩn, biến thể, prompt cho ảnh AI | Ảnh AI: công cụ tạo ảnh riêng; chỉnh kéo-thả: Canva (kết nối lại) | Claude không tự sinh ảnh chụp thực tế; ảnh sản phẩm/địa điểm dùng ảnh thật |
| 4. Video | Trung bình | Kịch bản, shot list, prompt, phụ đề, cắt/ghép/nén bằng ffmpeg | Tạo video AI: công cụ ngoài (như Google Flow/Veo, Kling...) hoặc điều khiển trình duyệt; giọng đọc: công cụ TTS ngoài hoặc chạy trên máy cá nhân | Không tự sinh video AI trong chat; giọng đọc trực tuyến không chạy được trong môi trường này |
| 5. Fanpage Chatbot | Trung bình | Kịch bản hội thoại, kho kiến thức, bộ trả lời bình luận, mã webhook mẫu, cấu hình no-code, kịch bản kiểm thử | Nền tảng chatbot (Botcake, ManyChat...) hoặc máy chủ + duyệt ứng dụng Meta; quyền quản trị page | Claude không "trực page" liên tục; chính sách cửa sổ nhắn tin của Meta |
| 6. Zalo CSKH | Trung bình đến Thấp | Bảng quy trình theo giai đoạn, kịch bản tin, nhãn khách, soạn tin trả lời | Zalo OA + API/ZNS (mẫu tin phải được duyệt), Make/n8n, bảng tính/CRM | Tự động hóa Zalo cá nhân thường trái điều khoản, có rủi ro khóa tài khoản |
| 7. Website và Landing Page | Cao | Viết nội dung, dựng trang HTML, xuất bản (Artifact hoặc Vercel nếu đã kết nối), form → Sheets/Make | Tên miền, cổng thanh toán (payOS, SePay, Casso... theo điều kiện hiện hành), tài khoản người bán | Claude không nhập thông tin thanh toán; thanh toán thật cần tài khoản merchant của bạn |
| 8. Quảng cáo | Trung bình | Tính hòa vốn, cấu trúc chiến dịch, bộ mẫu quảng cáo, quy tắc tự động, phân tích số liệu bạn dán | Quyền vào tài khoản quảng cáo (tự thao tác); tùy chọn dịch vụ đọc số liệu bên thứ ba | Cố ý không tự bật/tăng ngân sách; không đảm bảo ROAS |
| 9. Email Marketing | Cao (thiết kế, viết), Trung bình (gửi tự động) | Sơ đồ chuỗi, viết đủ email, phân nhóm, hướng dẫn SPF/DKIM/DMARC | Công cụ email marketing (Brevo, MailerLite, Mailchimp...), tên miền riêng | Gmail chỉ tạo bản nháp; không dùng Gmail cá nhân gửi hàng loạt |
| 10. Báo cáo | Cao (với dữ liệu xuất file) | Tổng hợp CSV/Excel thành Excel có công thức + tóm tắt + biểu đồ (đã thử: khớp số, 0 lỗi công thức) | Tự động kéo số: Make/n8n vào Google Sheets, hoặc dịch vụ bên thứ ba | Không tự đăng nhập tài khoản quảng cáo/phần mềm bán hàng; tổng đơn giữa các nền tảng có thể trùng |

## Việc Claude không làm (cố ý)

- Tự chi tiền quảng cáo, tự tăng ngân sách, tự gửi tin/email hàng loạt, tự đăng bài công khai khi chưa được xác nhận từng thao tác.
- Xử lý mật khẩu, OTP, token, số thẻ.
- Cam kết kết quả bán hàng hay ROAS.

## Ghép đường đi tự động ("chạy không cần ngồi canh")

Claude thiết kế và dựng; các khâu chạy liên tục dùng: nền tảng chatbot (fanpage), Zalo OA, công cụ email marketing, Make/n8n (nối form → bảng tính → thông báo, kéo số báo cáo hằng ngày), hosting (Vercel/Netlify). Khi người dùng muốn "tự động hoàn toàn", hỏi họ chọn công cụ nào rồi thiết kế theo công cụ đó, và đề xuất bắt đầu ở mức **nhắc việc/soạn nháp có người duyệt** trước khi bật tự gửi.
