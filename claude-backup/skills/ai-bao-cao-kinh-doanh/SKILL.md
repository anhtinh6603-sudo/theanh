---
name: ai-bao-cao-kinh-doanh
description: Tổng hợp báo cáo kinh doanh - doanh thu, số đơn, số khách/lead, chi phí quảng cáo và hiệu quả từng kênh (CPA, CPL, ROAS, tỷ lệ chốt, lợi nhuận sau quảng cáo), so sánh kỳ trước, cảnh báo kênh lỗ, và đề xuất bước tối ưu. Nhận số liệu từ file CSV/Excel hoặc dán trực tiếp, xuất file Excel có công thức, tóm tắt và biểu đồ. Dùng skill này khi người dùng muốn làm báo cáo tuần/tháng, xem kênh nào hiệu quả, tính ROAS/CPA, hỏi "tiền quảng cáo đi đâu", "doanh thu tháng này thế nào", tổng hợp số liệu Facebook/TikTok/Google/Zalo/sàn, hoặc dán bảng số liệu nhờ phân tích - kể cả khi không nói chữ báo cáo.
---

# Báo cáo kinh doanh theo kênh

Báo cáo tốt không phải bảng đẹp mà là **giúp quyết định tuần sau làm gì**: kênh nào tăng tiền, kênh nào giảm, việc gì phải kiểm tra. Skill này biến số liệu thô thành báo cáo có con số đúng, cảnh báo rõ và khuyến nghị có điều kiện.

## Bước 0 - Hỏi nhanh (gộp một lượt, tối đa 5 câu, bỏ câu đã biết)

1. Kỳ báo cáo (tuần/tháng/tùy chọn) và các kênh cần xem (Facebook Ads, TikTok Ads, Google Ads, Zalo, inbox tự nhiên, sàn...)?
2. Số liệu đang ở đâu: xuất từ trình quản lý quảng cáo, Google Sheets, sổ đơn hàng, phần mềm bán hàng?
3. Có biết **giá vốn**, **ROAS hòa vốn**, **CPA mục tiêu** chưa? (Nếu chưa, giúp tính trước theo skill `xay-chay-quang-cao-tu-dong`.)
4. Ai đọc báo cáo (chủ doanh nghiệp, đối tác, nhân viên) và họ cần quyết định gì?
5. Muốn báo cáo một lần hay lặp lại hằng tuần?

## Bước 1 - Lấy số liệu (nói rõ giới hạn)

Claude **không tự đăng nhập** tài khoản quảng cáo hay phần mềm bán hàng. Các cách lấy số, từ đơn giản đến tự động:

1. **Tải file lên/dán bảng** (CSV, Excel): cách nhanh nhất, làm được ngay.
2. **Google Sheets/Drive**: nếu đã kết nối Google Drive thì đọc file trên Drive.
3. **Tự động hóa bên ngoài**: Make/n8n kéo số hằng ngày vào một Google Sheets, sau đó phân tích từ sheet đó.
4. **Dịch vụ tổng hợp số liệu quảng cáo của bên thứ ba** (ví dụ Supermetrics, Windsor.ai): có connector nhưng là dịch vụ riêng, thường trả phí, người dùng tự kết nối và cấp quyền.

## Bước 2 - Chuẩn hóa dữ liệu

Bảng chuẩn (một dòng = một ngày x một kênh). Tên cột tiếng Việt hoặc tiếng Anh đều được, không phân biệt dấu:

| Cột | Ý nghĩa | Bắt buộc |
|---|---|---|
| `ngay` | Ngày | nên có (để so sánh kỳ) |
| `kenh` | Tên kênh | có |
| `chi_phi` | Chi phí quảng cáo | có |
| `doanh_thu` | Doanh thu ghi nhận | có |
| `don_hang` | Số đơn | nên có |
| `lead` | Khách tiềm năng (tin nhắn, số điện thoại) | nên có |
| `click`, `hien_thi` | Lượt bấm, lượt hiển thị | tùy chọn |
| `gia_von` | Tổng giá vốn của các đơn | tùy chọn (để tính lợi nhuận) |

Xem file mẫu `assets/mau-du-lieu.csv` (**dữ liệu giả để thử**, không phải số thật). Số kiểu Việt `1.500.000` được hiểu là 1500000.

Trước khi tính, **kiểm tra chất lượng dữ liệu** và nói rõ với người dùng: có dòng trùng không, khoảng ngày đầy đủ không, đơn vị tiền có thống nhất không, kênh có bị đặt tên khác nhau cho cùng một thứ không (ví dụ "FB" và "Facebook Ads"), có ô trống bất thường không.

## Bước 3 - Chạy công cụ tổng hợp

```
python scripts/bao_cao.py --input du-lieu.csv --out-dir bao-cao \
  --title "Báo cáo tuần 38" --breakeven-roas 2.5 --target-cpa 150000 --compare-days 7
```

Đầu ra: `bao-cao-hieu-qua.xlsx` (sheet dữ liệu + sheet tổng hợp theo kênh bằng **công thức**, đổi số là tự tính lại), `tom-tat.md` (tổng quan, bảng kênh, cảnh báo, so sánh kỳ), `bieu-do-theo-kenh.png`. Cần Python với pandas, openpyxl, matplotlib.

Lưu ý: file Excel mới tạo chưa lưu sẵn giá trị đã tính; mở bằng Excel/Google Sheets sẽ tự tính. Nếu cần đọc giá trị bằng công cụ khác, dùng `recalc.py` của skill `xlsx` (nếu có) để tính lại. **Luôn đối chiếu tổng với số gốc** trước khi giao: cộng tay tổng chi phí và tổng doanh thu, so với dòng TỔNG của báo cáo.

## Bước 4 - Định nghĩa chỉ số (viết rõ trong báo cáo)

- **ROAS** = doanh thu / chi phí quảng cáo. **CPA** = chi phí / số đơn. **CPL** = chi phí / số lead.
- **CTR** = click / hiển thị. **CPC** = chi phí / click. **Giá trị đơn TB** = doanh thu / số đơn.
- **Tỷ lệ chốt** = đơn / lead.
- **Lợi nhuận sau quảng cáo** = doanh thu − giá vốn − chi phí quảng cáo (chưa gồm lương, mặt bằng, thuế, phí sàn: nói rõ).
- Kênh không chi tiền (inbox, giới thiệu) không có CPA/ROAS; hiển thị "-" chứ không phải 0.

## Bước 5 - Viết báo cáo cho người ra quyết định

Cấu trúc gợi ý:
1. **Tóm tắt điều hành** (3-5 dòng): kết quả chính, kênh tốt nhất/tệ nhất, một việc cần làm ngay.
2. **Bảng theo kênh** và biểu đồ.
3. **So sánh với kỳ trước** (tăng/giảm bao nhiêu %, nguyên nhân có thể).
4. **Điểm cần chú ý**: kênh dưới hòa vốn, kênh chi tiền không ra đơn, CPA vượt mục tiêu, thay đổi bất thường.
5. **Khuyến nghị (tối đa 3)**, mỗi cái có điều kiện và cách kiểm chứng. Ví dụ: "Giảm 30% ngân sách nhóm X nếu CPA vẫn trên mức mục tiêu sau 3 ngày nữa", chứ không phải "tắt kênh X".
6. **Điều chưa chắc**: dữ liệu thiếu, kỳ ngắn, theo dõi có thể lệch.

Phân biệt rõ **quan sát** (có trong số liệu) và **suy đoán** (nguyên nhân có thể). Số đơn ít (ví dụ dưới khoảng 30 đơn/kênh) thì tỷ lệ dao động mạnh: nói thẳng "chưa đủ dữ liệu để kết luận".

## Rào chắn

- Chỉ dùng số liệu người dùng cung cấp. **Không bịa, không nội suy, không làm tròn để đẹp.** Thiếu cột nào thì chỉ số liên quan để trống và nói rõ.
- Mỗi nền tảng tự ghi nhận đơn nên tổng đơn các kênh có thể **trùng**; ưu tiên số đơn thật từ hệ thống bán hàng và nêu sự khác biệt.
- Không đưa thông tin cá nhân của khách (tên, số điện thoại, địa chỉ) vào báo cáo; chỉ dùng số tổng hợp.
- Không tự gửi báo cáo cho người khác, không tạo lịch gửi tự động khi chưa được xác nhận. Không nhờ dán mật khẩu/khóa API vào chat.
- Khuyến nghị chi tiền/tăng ngân sách chỉ là gợi ý vận hành, không đảm bảo kết quả.

## Kiểm tra cuối

Tổng chi phí, doanh thu, đơn khớp số gốc? Mọi chỉ số có công thức rõ và không chia cho 0? Cảnh báo có dựa trên ngưỡng người dùng đặt (ROAS hòa vốn, CPA mục tiêu) hay chỉ là ước đoán? Đã nói rõ giới hạn dữ liệu?
