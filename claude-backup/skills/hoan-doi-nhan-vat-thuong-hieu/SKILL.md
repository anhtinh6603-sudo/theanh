---
name: hoan-doi-nhan-vat-thuong-hieu
description: Hoán đổi nhân vật trong ảnh tham chiếu bằng gương mặt và trang phục thương hiệu cố định của “cô gái áo vàng”, đồng thời bám sát bối cảnh, bố cục, góc máy, đạo cụ, ánh sáng và tỷ lệ ảnh gốc. Dùng khi người dùng nói “Tạo cho cô gái áo vàng một hình ảnh tương tự hình ảnh tham chiếu”, “hoán đổi nhân vật”, “thay nhân vật bằng mặt thương hiệu”, “khóa mặt cô gái áo vàng”, “giữ nguyên trang phục thương hiệu”, hoặc gửi một hay nhiều ảnh tham chiếu để tạo thành bộ ảnh tương ứng.
---

# Hoán Đổi Nhân Vật Thương Hiệu

## Mục tiêu

Dùng `assets/co-gai-ao-vang-face-brand.jpg` làm nguồn nhận diện và trang phục cố định. Hiểu cụm “cô gái áo vàng” là tên gọi của nhân vật thương hiệu và luôn giữ nguyên bộ trang phục trong ảnh này: áo quây vàng có chữ “KOL AI GO GLOBAL”, chân váy dài dệt màu trắng, vòng cổ và vòng tay. Không thay bằng trang phục của ảnh tham chiếu.

Đặt nhân vật thương hiệu vào bối cảnh của ảnh tham chiếu. Bám sát các yếu tố còn lại của từng ảnh tham chiếu ở mức cao nhất có thể nhưng không sao chép trang phục của nhân vật tham chiếu.

## Quy trình

1. Kiểm tra đã có ít nhất một ảnh tham chiếu. Nếu chưa có, yêu cầu người dùng gửi ảnh.
2. Xem kỹ ảnh mặt thương hiệu và từng ảnh tham chiếu trước khi tạo.
3. Với mỗi ảnh tham chiếu, phân tích riêng:
   - tỷ lệ khung hình, cỡ cảnh, tiêu cự cảm nhận và góc máy;
   - vị trí nhân vật, tư thế, hướng nhìn và biểu cảm;
   - kiểu tóc, tư thế phù hợp, phụ kiện bối cảnh và đạo cụ;
   - kiến trúc, nội thất, phong cảnh, vật thể tiền cảnh và hậu cảnh;
   - thời điểm, ánh sáng, bảng màu, độ sâu trường ảnh và phong cách xử lý.
4. Dùng công cụ tạo/chỉnh sửa ảnh với đúng hai nguồn cho mỗi kết quả: ảnh mặt thương hiệu cố định và một ảnh tham chiếu. Tạo từng ảnh riêng để không trộn chi tiết giữa các tham chiếu.
5. Trong chỉ dẫn tạo ảnh, nêu rõ:
   - thay duy nhất nhận diện khuôn mặt của nhân vật bằng gương mặt thương hiệu;
   - giữ ổn định các đặc điểm nhận diện chính của gương mặt thương hiệu;
   - giữ nguyên áo quây vàng có chữ, chân váy dài trắng, vòng cổ và vòng tay từ ảnh thương hiệu;
   - lấy kiểu tóc, tư thế phù hợp, bối cảnh, bố cục, góc máy, đạo cụ và ánh sáng từ ảnh tham chiếu;
   - nếu tư thế hoặc hoạt động trong ảnh tham chiếu không phù hợp với trang phục dài, giữ đúng không gian và góc nhìn nhưng chuyển sang tư thế kín đáo, tự nhiên và an toàn; không đổi sang đồ bơi, đồ ngủ hoặc trang phục khác;
   - không ghép hai khuôn mặt, không giữ nét nhận diện của nhân vật gốc, không thêm người hoặc vật thể ngoài yêu cầu;
   - không tự thêm chữ, logo, watermark, giá hoặc thông điệp quảng cáo;
   - chỉ tái tạo chữ nhìn thấy trong ảnh khi người dùng yêu cầu rõ, và không sửa chính tả theo suy đoán.
6. Giữ nguyên tỷ lệ ảnh tham chiếu nếu người dùng không chỉ định tỷ lệ khác.
7. Với 10 ảnh tham chiếu, tạo 10 kết quả theo đúng thứ tự 1–10 và đối chiếu từng kết quả với đúng ảnh nguồn.

## Thứ tự ưu tiên

1. Nhận diện gương mặt thương hiệu nhất quán.
2. Bối cảnh, bố cục và góc máy của ảnh tham chiếu.
3. Trang phục thương hiệu cố định, không thay đổi hay sáng tạo thêm.
4. Tư thế phù hợp, phụ kiện, đạo cụ, ánh sáng, màu sắc và độ chân thực.

Không biến ảnh thành một concept mới. Không đổi địa điểm, mùa, thời tiết, nội thất hoặc phong cách nếu người dùng không yêu cầu.

## Câu lệnh chuẩn

Khi người dùng nói:

> Tạo cho cô gái áo vàng một hình ảnh tương tự hình ảnh tham chiếu

Hiểu là: dùng gương mặt và nguyên bộ trang phục trong `assets/co-gai-ao-vang-face-brand.jpg` cho nhân vật, còn bối cảnh, bố cục, góc máy, ánh sáng và đạo cụ của ảnh mới phải bám sát ảnh tham chiếu.

## Kiểm tra trước khi trả kết quả

- Đúng gương mặt thương hiệu, không lai với nhân vật tham chiếu.
- Đúng số lượng và đúng thứ tự ảnh.
- Trang phục thương hiệu giữ nguyên; bối cảnh, khung hình, góc máy và đạo cụ bám sát từng tham chiếu.
- Không có chi tiết thừa, chữ thừa, tay chân thừa, biến dạng hoặc vật thể bị nhân đôi.
- Không hứa “giống 100%”; nếu một chi tiết chưa sát, ưu tiên tạo lại ảnh đó dựa trên đúng hai nguồn tương ứng.
