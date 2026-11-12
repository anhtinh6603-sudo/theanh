---
name: xay-zalo-cham-soc-khach-tu-dong
description: Xây dựng quy trình chăm sóc khách hàng tự động trên Zalo theo từng giai đoạn (mới quan tâm, tư vấn, chốt đơn, sau mua, tái mua, khách nguội) - gồm bảng quy trình, kịch bản tin nhắn, cách gắn nhãn khách, kết nối Zalo OA với bảng tính/CRM/Make, quy tắc tần suất và dừng. Dùng skill này khi người dùng muốn tự động hóa chăm sóc khách qua Zalo, làm Zalo OA, ZNS, nhắn tin nhắc lịch/nhắc mua lại, follow-up khách, phễu Zalo, hoặc "làm sao để Zalo tự chăm khách theo quy trình" - kể cả khi không nói chữ OA. Không dùng cho việc chỉ soạn một tin trả lời (đó là skill zalo-tra-loi-khach).
---

# Xây quy trình chăm sóc khách hàng tự động trên Zalo

Đây là skill thiết kế **cả quy trình**: khách đi qua những giai đoạn nào, ở mỗi giai đoạn nhận tin gì, lúc nào, và khi nào dừng. Để soạn từng tin theo giọng chủ tài khoản, dùng kèm skill `zalo-tra-loi-khach` nếu người dùng đã cài.

## Chọn kênh trước: OA hay tài khoản cá nhân

- **Zalo OA (Official Account)** là kênh chính thống để tự động hóa: có API, có mẫu tin thông báo (ZNS) cần được duyệt, có quy định riêng về loại tin và khung thời gian được nhắn. Khuyến nghị dùng OA cho mọi quy trình tự động.
- **Tài khoản Zalo cá nhân**: các công cụ điều khiển ứng dụng để tự gửi tin thường trái điều khoản dịch vụ, có rủi ro bị hạn chế/khóa tài khoản và lộ nội dung chat. Nếu người dùng vẫn muốn, nói rõ rủi ro một lần, và chỉ đề xuất chế độ **soạn nháp rồi duyệt tay**, không tự gửi hàng loạt.

Quy định, hạn mức và giá của Zalo OA/ZNS thay đổi theo thời gian: nếu có công cụ tìm web, đối chiếu với tài liệu chính thức của Zalo trước khi khẳng định.

## Bước 0 - Hỏi nhanh (gộp một lượt, tối đa 5 câu)

1. Bán gì; khách mua một lần hay mua lặp lại; chu kỳ mua thường bao lâu?
2. Khách đến từ đâu (fanpage, quảng cáo, khách vãng lai, giới thiệu) và hiện lưu thông tin ở đâu (Zalo, Excel/Google Sheets, CRM)?
3. Đã có Zalo OA chưa? Ai trực và giờ nào?
4. Mục tiêu ưu tiên: tăng chốt đơn, giảm bỏ sót, nhắc lịch hẹn, hay kéo khách cũ quay lại?
5. Muốn tự động đến mức nào: chỉ nhắc việc cho nhân viên, soạn nháp, hay tự gửi?

## Bước 1 - Thiết kế phễu theo giai đoạn

Lập bảng, mỗi dòng một bước tự động:

| Giai đoạn | Điều kiện kích hoạt | Tin gửi | Thời điểm | Điều kiện dừng | Ai xử lý |
|---|---|---|---|---|---|
| Mới quan tâm | Khách vừa nhắn/quan tâm OA | Chào ngắn + hỏi nhu cầu | Ngay | Khách trả lời | Bot/người |
| Đang tư vấn | Đã nêu nhu cầu | Thông tin đúng nhu cầu + bước tiếp | Ngay | Khách đồng ý/từ chối | Người + gợi ý |
| Chưa chốt | 24-48 giờ im lặng | Một tin hỏi vướng mắc | Trong giờ hợp lý | Khách trả lời | Bot nhắc người |
| Vừa mua | Đã thanh toán/đặt | Xác nhận + hướng dẫn | Ngay | - | Tự động |
| Sau mua | Vài ngày sau khi nhận | Hỏi trải nghiệm, xin phản hồi | Theo chu kỳ | Khách phản hồi | Tự động + người |
| Tái mua | Gần hết chu kỳ mua | Nhắc mua lại/ưu đãi thật | Theo chu kỳ | Khách mua/từ chối | Tự động |
| Khách nguội | Lâu không tương tác | Một tin nhẹ, có lý do rõ | Thưa, không dồn dập | Khách phản hồi/xin ngừng | Tự động |

Điền đủ thời điểm và nội dung theo ngành của người dùng, không để bảng chung chung.

## Bước 2 - Gắn nhãn và quy tắc chuyển giai đoạn

Đề xuất bộ nhãn tối giản (ví dụ: moi, dang-tu-van, cho-chot, da-mua, khach-cu, khong-lam-phien) và quy tắc: sự kiện nào đổi nhãn nào. Mỗi khách chỉ ở **một** giai đoạn tại một thời điểm. Nhãn "không làm phiền" phải chặn mọi tin chủ động.

## Bước 3 - Kịch bản tin nhắn

Viết sẵn từng tin theo bảng trên. Quy tắc giọng (giống chat thật):
- Ngắn, 1-3 câu; câu đầu vào thẳng việc; tối đa một câu hỏi mỗi tin.
- Không giọng tổng đài, không công thức "mình hỗ trợ bạn nhé".
- Mỗi tin chủ động phải có **lý do với khách** (nhắc lịch, nhắc dùng hết, hỏi vướng mắc), không nhắn chỉ để "giữ nhịp".
- Không bịa giá, ưu đãi, thời hạn. Chỉ dùng dữ liệu người dùng cung cấp.

## Bước 4 - Kết nối kỹ thuật (nếu người dùng muốn tự động thật)

Mô tả kiến trúc theo mức độ:
1. **Mức 1 - Nhắc việc**: bảng Google Sheets có cột giai đoạn/ngày liên hệ tiếp; công thức lọc "hôm nay cần chăm ai"; nhân viên gửi tay. Ít rủi ro nhất.
2. **Mức 2 - Bán tự động**: Make/n8n đọc bảng, soạn nháp tin, gửi thông báo cho nhân viên duyệt.
3. **Mức 3 - Tự gửi qua OA**: webhook nhận sự kiện từ OA, cập nhật nhãn, gửi tin theo mẫu đã duyệt. Cần ứng dụng Zalo, quyền API, và xử lý lỗi/gửi lại.

Nếu người dùng đã kết nối Make hoặc Google Drive/Sheets, đề xuất dùng; **không tạo hay bật kịch bản chạy thật khi chưa được xác nhận**. Không nhờ dán khóa API/token vào chat.

## Rào chắn

- **Tần suất**: mặc định tối đa 1 tin chủ động mỗi 48 giờ cho khách đang tư vấn, và không quá 2 tin mỗi tháng cho khách nguội. Nhắn trong khung giờ hợp lý (khoảng 8h-20h).
- **Dừng ngay** khi khách nói không cần/đừng nhắn, và ghi nhãn "không làm phiền".
- Chỉ nhắn người đã tương tác hoặc đồng ý nhận. Không nhập danh sách số điện thoại mua sẵn. Tuân thủ quy định chống tin nhắn rác và bảo vệ dữ liệu cá nhân của Việt Nam (kiểm tra văn bản hiện hành).
- Nếu khách hỏi có phải bot không thì trả lời thật.
- Chuyển người thật khi khách giận, khiếu nại, hoàn tiền, hoặc hỏi ngoài dữ liệu đã có.

## Đo lường

Tỷ lệ khách phản hồi từng giai đoạn, tỷ lệ chốt, số khách xin ngừng nhắn (chỉ số cảnh báo: nếu tăng thì giảm tần suất), thời gian từ tin đầu đến chốt.

## Kiểm tra cuối

Bảng quy trình có đủ điều kiện dừng ở mỗi dòng? Mọi tin có lý do rõ ràng? Đã có bước chạy thử với 3-5 khách nội bộ trước khi bật thật? Đã nói rõ phần nào cần đối chiếu lại với tài liệu chính thức của Zalo?
