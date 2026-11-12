---
name: xay-chay-quang-cao-tu-dong
description: Xây dựng quy trình chạy quảng cáo tự động (Facebook/Meta Ads, TikTok Ads, Google Ads) - tính điểm hòa vốn (CPA, ROAS), thiết kế cấu trúc chiến dịch test-rồi-scale, viết bộ mẫu quảng cáo theo nhiều góc tiếp cận, cài đo lường Pixel/CAPI/UTM, thiết lập quy tắc tự động và báo cáo hằng ngày, quy trình tối ưu hằng tuần với ngưỡng quyết định rõ ràng. Dùng skill này khi người dùng muốn chạy quảng cáo, tối ưu quảng cáo, tự động hóa ads, làm báo cáo quảng cáo, viết content quảng cáo, hoặc hỏi "quảng cáo tốn tiền mà không ra đơn" - kể cả khi không nói tên nền tảng.
---

# Xây quy trình chạy quảng cáo tự động

Quảng cáo tự động không có nghĩa là "bật lên rồi để mặc". Nó là một quy trình có **con số hòa vốn, ngưỡng dừng, ngưỡng tăng và người chịu trách nhiệm quyết định**. Skill này giúp dựng quy trình đó và viết sẵn nội dung; **mọi thao tác chi tiền do người dùng tự bật hoặc xác nhận**.

## Nguyên tắc về tiền

- Claude không tự bật, tăng ngân sách hay tạo chiến dịch thật nếu chưa được người dùng xác nhận rõ từng thao tác. Không nhờ dán mật khẩu, token hay thông tin thẻ vào chat.
- Không hứa ROAS hay số đơn. Kết quả phụ thuộc sản phẩm, giá, sáng tạo và thị trường; nói rõ đây là hướng dẫn vận hành, không đảm bảo kết quả.
- Luôn đặt **trần chi tiêu** mỗi ngày và tổng ngân sách thử nghiệm mà người dùng chấp nhận mất.

## Bước 0 - Hỏi nhanh (gộp, tối đa 6 câu)

1. Sản phẩm, giá bán, giá vốn, phí ship/vận hành mỗi đơn?
2. Mục tiêu: đơn hàng, lead (số điện thoại), tin nhắn, hay nhận diện?
3. Nền tảng đã có tài khoản; đã có Pixel/Trang đích/Fanpage chưa?
4. Ngân sách thử mỗi ngày và số ngày chịu được?
5. Đã từng chạy chưa; nếu có, kết quả và điều học được?
6. Có ảnh/video/đánh giá thật để làm sáng tạo không?

## Bước 1 - Tính điểm hòa vốn (bắt buộc làm trước)

Tính cho người dùng, hiển thị phép tính:
- **Lợi nhuận gộp mỗi đơn** = giá bán − giá vốn − phí ship/vận hành/hoa hồng.
- **CPA hòa vốn** = lợi nhuận gộp mỗi đơn (chi quá số này cho một đơn là lỗ).
- **ROAS hòa vốn** = giá bán ÷ lợi nhuận gộp mỗi đơn (tương đương 1 ÷ biên lợi nhuận gộp).
- **CPA mục tiêu**: thấp hơn CPA hòa vốn, chừa biên (ví dụ 60-70% CPA hòa vốn) để có lãi. Tính tỷ lệ đơn hủy/hoàn vào phép tính nếu bán COD.

Nếu CPA hòa vốn quá thấp so với chi phí thông thường của ngành, nói thẳng và gợi ý sửa mô hình (tăng giá trị đơn, combo, bán thêm) trước khi đổ tiền vào ads.

## Bước 2 - Cấu trúc chiến dịch: test rồi scale

1. **Giai đoạn test sáng tạo**: ít nhóm quảng cáo, nhắm rộng hợp lý, mỗi nhóm 3-5 mẫu quảng cáo khác **góc tiếp cận**, không chỉ khác màu sắc.
2. **Giai đoạn chọn lọc**: giữ mẫu thắng, tắt mẫu thua theo ngưỡng dưới đây.
3. **Giai đoạn scale**: tăng ngân sách từng nấc nhỏ; mở rộng tệp/định dạng; tiếp thị lại người đã xem/nhắn/thêm giỏ.

Tài khoản mới hoặc ngân sách nhỏ: cấu trúc càng đơn giản càng tốt. Kiểm tra cách nền tảng gọi tên các mục tiêu và tính năng hiện hành, vì giao diện thay đổi thường xuyên.

## Bước 3 - Bộ mẫu quảng cáo

Viết sẵn cho người dùng, mỗi góc tiếp cận một bộ: **hook (câu mở/3 giây đầu)**, nội dung chính, tiêu đề, kêu gọi hành động, và gợi ý hình ảnh/video. Các góc thường dùng: giải quyết nỗi đau, kết quả mong muốn, so sánh với cách cũ, câu chuyện khách hàng thật, phá bỏ hiểu lầm, ưu đãi thật có thời hạn thật. Trang đích phải khớp lời hứa trong quảng cáo.

## Bước 4 - Đo lường trước khi chi tiền

Cài Pixel (và Conversions API nếu có điều kiện), GA4, sự kiện chuyển đổi đúng mục tiêu; gắn UTM đặt tên thống nhất (nguồn - chiến dịch - nhóm - mẫu). Chạy thử một chuyển đổi để chắc sự kiện ghi nhận. Không có đo lường đúng thì đừng bật ngân sách.

## Bước 5 - Quy tắc tự động và báo cáo

Ví dụ quy tắc (đặt bằng tính năng quy tắc tự động của nền tảng, người dùng duyệt từng quy tắc):
- Dừng mẫu quảng cáo khi chi tiêu vượt khoảng 2-3 lần CPA mục tiêu mà chưa có chuyển đổi.
- Thông báo (không tự tắt) khi CPA vượt CPA hòa vốn liên tục một số ngày.
- Chỉ tăng ngân sách khi CPA đạt mục tiêu qua nhiều ngày, mỗi lần tăng khoảng 20% để tránh phá vỡ tối ưu.
- Trần chi tiêu ngày/tổng để chặn thất thoát.

Báo cáo hằng ngày: kéo số từ nền tảng vào Google Sheets (báo cáo xuất tự động hoặc Make/API), một bảng gồm chi tiêu, đơn, CPA, ROAS, tần suất, ghi chú. Mục đích là **quyết định**, không phải để đẹp.

## Bước 6 - Nhịp tối ưu hằng tuần

Mỗi tuần một lần: xem mẫu thắng/thua, rút bài học (góc nào hiệu quả), sinh mẫu mới dựa trên góc thắng, kiểm tra trang đích và tỷ lệ chốt đơn phía sau (quảng cáo tốt mà chốt yếu là lỗi ở khâu sau). Không thay đổi lớn liên tục vì mỗi thay đổi làm nền tảng học lại.

## Rào chắn chính sách

- Không cam kết kết quả, không "trước/sau" gây hiểu lầm, không tuyên bố y tế/thu nhập không có căn cứ, không nhắm bằng thuộc tính nhạy cảm, không dùng hình ảnh người nổi tiếng hay đánh giá giả.
- Ngành nhạy cảm (sức khỏe, tài chính, làm đẹp, tuyển dụng...) có chính sách riêng: kiểm tra chính sách quảng cáo hiện hành của nền tảng và nói rõ nếu nội dung có nguy cơ bị từ chối.
- Nội dung do AI tạo mà trông như thật: gắn nhãn nếu nền tảng yêu cầu.

## Kiểm tra cuối

Đã có CPA/ROAS hòa vốn bằng số cụ thể? Đã có trần chi tiêu và người quyết định mọi thao tác chi tiền? Đo lường chạy thử được? Mọi lời hứa trong quảng cáo có căn cứ và khớp trang đích?
