---
name: xay-fanpage-chatbot-tu-dong
description: Xây dựng chatbot tự động cho fanpage Facebook (Messenger) - thiết kế kịch bản hội thoại, bộ câu trả lời mẫu, luồng thu số điện thoại/chốt đơn/đặt lịch, tự động trả lời bình luận, chuyển cho người thật, chọn nền tảng no-code hoặc tự dựng bằng API, và bộ kịch bản kiểm thử. Dùng skill này bất cứ khi nào người dùng muốn làm chatbot cho fanpage, tự động trả lời inbox, bot Messenger, trả lời bình luận tự động, chốt đơn qua inbox, hoặc nhắc tới Botcake, ManyChat, Chatfuel, Pancake - kể cả khi họ chỉ nói "page bị ngợp tin nhắn" hay "muốn AI trả lời khách trên Facebook".
---

# Xây chatbot tự động cho fanpage Facebook

Mục tiêu của chatbot fanpage không phải "trả lời thay người", mà làm tốt ba việc: **trả lời nhanh những câu lặp lại, phân loại khách, và thu lead/chốt đơn** - rồi chuyển cho người thật đúng lúc. Bot càng ngắn, càng thẳng vào việc thì khách càng ở lại.

Người dùng thường không rành kỹ thuật: giải thích thuật ngữ bằng một câu ngắn (webhook, token, App Review...) và luôn đưa từng bước bấm cụ thể.

## Bước 0 - Hỏi nhanh (gộp một lượt, tối đa 5 câu, bỏ câu đã biết)

1. Bán gì / dịch vụ gì, khách điển hình là ai?
2. Mục tiêu chính của bot: lấy số điện thoại, chốt đơn, đặt lịch/đặt phòng, hay hỗ trợ sau bán?
3. Đã có gì sẵn: bảng giá, câu hỏi hay gặp, ảnh/video sản phẩm, người trực page?
4. Mức kỹ thuật và ngân sách: chỉ muốn kéo-thả no-code, hay sẵn sàng có server/code?
5. Lượng tin nhắn mỗi ngày (ước lượng) và giờ có người trực.

## Bước 1 - Chọn hướng làm

| Hướng | Hợp khi | Đánh đổi |
|---|---|---|
| A. No-code (Botcake, ManyChat, Chatfuel, Pancake...) | Người mới, cần chạy trong vài ngày, luồng theo nút bấm | Ít linh hoạt; trả phí theo số liên hệ |
| B. Tự dựng qua Messenger Platform API + webhook + mô hình AI | Cần AI trả lời tự do theo kiến thức riêng | Cần server, duyệt ứng dụng, bảo trì |
| C. A kết hợp Make/n8n/Google Sheets | Cần đẩy lead sang bảng tính/CRM, báo về điện thoại | Thêm một lớp cấu hình |

Mặc định khuyên **A hoặc C cho lần đầu**; chuyển sang B khi luồng nút bấm không còn đủ. Giá và tính năng của các nền tảng thay đổi nhanh: nếu có công cụ tìm web thì kiểm tra trang chính thức trước khi khẳng định giá hay giới hạn.

## Bước 2 - Thiết kế kịch bản (sản phẩm bàn giao chính)

Luôn giao đủ các phần sau, viết sẵn nội dung, không để khung trống:

1. **Sơ đồ luồng** dạng văn bản: Chào → hỏi nhu cầu (nút bấm) → nhánh (hỏi giá / xem sản phẩm / đặt hàng / hỏi khác) → thu thông tin → xác nhận → chuyển người hoặc kết thúc.
2. **Bộ tin mẫu**: chào mới, chào lại khách cũ, menu nhanh, FAQ (10-15 câu), hỏi nhu cầu, xin số điện thoại (nêu lý do xin), xác nhận đơn/lịch, nhắc lại khi khách im, ngoài giờ trực, chuyển người thật, không hiểu câu hỏi.
3. **Trả lời bình luận**: bảng từ khoá ("giá", "ib", "bao nhiêu", "địa chỉ"...) → câu trả lời công khai ngắn + mời nhắn tin. Mỗi bình luận nên có nhiều biến thể để không lặp y hệt.
4. **Kho kiến thức** (bảng): chủ đề - câu trả lời chuẩn - nguồn/ngày cập nhật. Bot chỉ được nói những gì có trong bảng này.
5. **Danh sách cấu hình** theo nền tảng đã chọn: kết nối page, quyền cần cấp, gắn thẻ (tag) khách, đẩy lead sang bảng tính.
6. **Bộ kiểm thử**: ít nhất 10 kịch bản (khách hỏi giá, hỏi ngoài luồng, nhắn sai chính tả, đòi gặp người, khách giận, spam, nhắn lúc nửa đêm...) kèm kết quả mong đợi.

Nếu chọn hướng B, thêm: mã webhook mẫu (xác minh chữ ký, trả lời trong thời gian ngắn), cách lưu bí mật bằng biến môi trường, hướng dẫn triển khai (dùng connector Vercel nếu người dùng đã kết nối, hoặc hướng dẫn thủ công), và prompt hệ thống cho phần AI.

## Nguyên tắc hội thoại của bot

- Tin ngắn, mỗi lượt một việc, tối đa một câu hỏi. Ưu tiên nút bấm cho lựa chọn, cho phép gõ chữ tự do bất cứ lúc nào.
- Trả lời đúng câu vừa hỏi ở câu đầu; không lặp lời chào giữa hội thoại.
- Không bịa giá, ưu đãi, tồn kho, chính sách. Không có dữ liệu thì nói chưa chắc và chuyển người.
- Nếu khách hỏi thẳng "bạn là bot à?", trả lời thật là tin nhắn có AI hỗ trợ.
- Giọng nói: nếu người dùng đã có skill soạn tin Zalo `zalo-tra-loi-khach`, dùng cùng bộ quy tắc giọng để hai kênh nhất quán.

## Chuyển cho người thật khi

Khách đòi gặp người, đang giận hoặc khiếu nại, hỏi hoàn tiền/pháp lý/y tế, xin giá đặc biệt hoặc số lượng lớn, hoặc bot trả lời sai/không hiểu 2 lần liên tiếp. Khi chuyển: tạm dừng bot cho hội thoại đó, báo chủ page (thông báo điện thoại hoặc email), và nói với khách một câu thật lòng về thời gian người thật phản hồi.

## Rào chắn chính sách và an toàn

- Messenger có **cửa sổ nhắn tin** sau lần khách nhắn gần nhất; nhắn chủ động ngoài cửa sổ bị giới hạn chặt. Kiểm tra chính sách Messenger Platform hiện hành trước khi thiết kế tin nhắn nhắc/quảng bá, và chỉ gửi cho người đã đồng ý nhận.
- Không gửi tin quảng cáo hàng loạt cho người chưa từng tương tác; không trả lời bình luận kiểu spam.
- Chỉ xin dữ liệu cần thiết (tên, số điện thoại, nhu cầu). Không xin số thẻ, mật khẩu, mã OTP. Có cách xoá dữ liệu khi khách yêu cầu.
- **Không bao giờ nhờ người dùng dán token, mật khẩu hay khoá API vào cuộc trò chuyện.** Hướng dẫn họ tự nhập vào ô cấu hình của nền tảng hoặc biến môi trường.
- Cấp quyền cho nền tảng bằng vai trò trên Meta Business, không chia sẻ mật khẩu tài khoản Facebook.

## Vận hành sau khi chạy

Tuần đầu đọc lại hội thoại thật mỗi ngày, ghi các câu bot trả lời hụt và bổ sung vào kho kiến thức. Theo dõi: số hội thoại, tỷ lệ khách để lại số điện thoại, tỷ lệ chuyển người, thời gian phản hồi. Sau đó xem lại mỗi tuần.

## Kiểm tra cuối trước khi giao

- Mọi con số, giá, link trong kịch bản đều lấy từ dữ liệu người dùng cung cấp?
- Có đường thoát sang người thật ở mọi nhánh?
- Đã có kịch bản test và hướng dẫn chạy thử bằng chính tài khoản của chủ page trước khi mở cho khách?
- Đã nói rõ phần nào chỉ đúng tại thời điểm viết và cần kiểm tra lại với tài liệu chính thức?
