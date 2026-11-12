---
name: ai-thiet-ke-quang-cao
description: Thiết kế hình ảnh marketing - ảnh quảng cáo Facebook/Instagram, poster, thumbnail YouTube, banner web, cover fanpage, story dọc, ảnh giới thiệu sản phẩm. Lập brief thiết kế, chọn cách làm (tạo ảnh có chữ tiếng Việt bằng công cụ có sẵn, viết prompt cho công cụ tạo ảnh AI, hoặc dùng Canva), xuất đúng kích thước từng nền tảng và kiểm tra chữ, độ tương phản, vùng an toàn. Dùng skill này khi người dùng cần làm ảnh quảng cáo, banner, poster, thumbnail, bìa fanpage, ảnh sản phẩm, "thiết kế giúp tôi", "làm cái ảnh để đăng", hoặc muốn ảnh đồng bộ nhận diện thương hiệu - kể cả khi họ không nói chữ thiết kế.
---

# Thiết kế hình ảnh marketing

Ảnh quảng cáo tốt làm được ba việc trong 2 giây: **dừng ngón tay đang lướt, nói rõ ưu đãi, và chỉ ra bước tiếp theo**. Skill này giúp làm ra ảnh dùng được ngay, không chỉ "ý tưởng thiết kế".

## Bước 0 - Hỏi nhanh (gộp một lượt, tối đa 5 câu, bỏ câu đã biết)

1. Ảnh dùng để làm gì và đăng ở đâu (bài Facebook, story, quảng cáo, thumbnail, banner web, poster in)?
2. Thông điệp chính: một câu ưu đãi/lợi ích, và hành động muốn khách làm (nhắn tin, gọi, đặt hàng)?
3. Thông tin phải có trên ảnh: giá, thời hạn, số điện thoại, địa chỉ, logo?
4. Nhận diện thương hiệu: màu chủ đạo, font, logo (file PNG nền trong), phong cách (sang trọng, gần gũi, trẻ trung)?
5. Có ảnh thật (sản phẩm, phòng, món ăn, người thật đã đồng ý) không, hay cần nền/hình minh họa do AI tạo?

## Bước 1 - Chọn cách làm (nói rõ cách nào làm được ngay, cách nào cần công cụ ngoài)

| Cách | Khi nào dùng | Claude làm được |
|---|---|---|
| **A. Dựng bằng công cụ trong skill** (`scripts/tao_banner.py`) | Ảnh chủ yếu là **chữ + nền màu/ảnh thật**: banner ưu đãi, thumbnail, story, bìa fanpage, poster chữ | Làm trọn vẹn: ra file PNG đúng kích thước, chữ tiếng Việt chuẩn |
| **B. Ảnh AI + chữ** | Cần hình nền/ảnh minh họa đẹp mà chưa có ảnh thật | Viết prompt tạo ảnh (không kèm chữ trong ảnh); người dùng tạo bằng công cụ ảnh AI của họ (hoặc skill tạo ảnh đã cài, nếu có), rồi dùng cách A để chèn chữ lên ảnh |
| **C. Canva** | Người dùng muốn tự chỉnh sửa tiếp bằng giao diện kéo-thả | Nếu đã kết nối Canva: tìm/tạo/xuất thiết kế; nếu kết nối hết hạn, nhắc người dùng kết nối lại. Nếu chưa có: đưa cấu trúc bố cục và nội dung chữ để họ dựng |
| **D. Bố cục HTML/SVG** | Cần bản vector, nhiều biến thể, hoặc bố cục phức tạp | Tạo file, xem thử, xuất |

**Giới hạn cần nói thật:** Claude không tự sinh ảnh chụp thực tế (ảnh người, phòng, món ăn) từ đầu. Ảnh sản phẩm/địa điểm thật nên dùng ảnh thật của người dùng; ảnh AI chỉ nên làm nền hoặc minh họa, và không được gây hiểu nhầm là ảnh thật của sản phẩm.

## Bước 2 - Lập brief ngắn trước khi làm

Viết 5 dòng để người dùng xác nhận (nếu họ đã rất rõ thì bỏ qua): **mục tiêu - thông điệp - chữ trên ảnh - phong cách/màu - kích thước cần xuất**. Chữ trên ảnh phải ngắn: tiêu đề 4-8 từ, một phụ đề, một nút hành động.

## Bước 3 - Kích thước theo nền tảng

| Preset trong công cụ | Kích thước | Dùng cho |
|---|---|---|
| `fb_post` | 1080x1080 | Bài Facebook/Instagram vuông |
| `fb_post_4x5` | 1080x1350 | Bài dọc chiếm nhiều màn hình feed |
| `fb_story` | 1080x1920 | Story/Reels (chừa vùng trên/dưới cho giao diện) |
| `yt_thumbnail` | 1280x720 | Thumbnail YouTube, bìa video ngang |
| `fb_cover` | 1640x624 | Ảnh bìa fanpage (chừa lề, ảnh đại diện che góc trái dưới) |
| `banner_web` | 1920x600 | Banner đầu trang web |
| `poster_a4` | 2480x3508 | Poster in A4 (300 dpi) |

Kích thước và vùng hiển thị của nền tảng thay đổi theo thời gian: nếu có công cụ tìm web, kiểm tra hướng dẫn chính thức trước khi khẳng định.

## Bước 4 - Dựng ảnh bằng công cụ trong skill

1. Sao chép `assets/mau-mo-ta.json`, sửa nội dung (preset, chữ, màu, ảnh nền, logo).
2. Chạy: `python scripts/tao_banner.py --spec mo-ta.json --out ten-anh.png` (cần Pillow).
3. Đọc phần `warnings` in ra: nó báo tiêu đề quá dài, chữ tương phản thấp, hoặc font thiếu tiếng Việt. Sửa rồi chạy lại.
4. **Xem ảnh thật** (mở file ra xem) trước khi giao: kiểm tra chữ không bị cắt/đè, dấu tiếng Việt rõ, không dòng lẻ một từ.
5. Nếu máy không có font tiếng Việt phù hợp, đặt đường dẫn font `.ttf` (Arial, Be Vietnam Pro, Noto Sans...) vào trường `font` và `font_bold`.

Các trường chính: `preset`, `title` (bắt buộc), `subtitle`, `badge` (nhãn nhỏ nổi bật như "GIẢM 30%"), `cta` (nút), `footer` (số điện thoại/địa chỉ), `background` (màu, gradient, hoặc `image` kèm `overlay` để làm tối nền cho chữ dễ đọc), `logo`, `colors`, `align`.

## Bước 5 - Viết prompt cho ảnh nền AI (cách B)

Khung: **chủ thể + bối cảnh + ánh sáng + góc chụp + phong cách + màu chủ đạo + "để trống vùng bên trái/trên cho chữ" + tỷ lệ khung**. Thêm điều cần tránh: "không chữ, không logo, không watermark". Ví dụ khung: "Phòng khách sạn hiện đại nhìn ra biển lúc hoàng hôn, ánh sáng ấm, chụp góc rộng, phong cách ảnh quảng cáo cao cấp, tông xanh và vàng, để trống nửa trái ảnh, không chữ, không logo, tỷ lệ 1:1." Chữ nên chèn ở bước sau bằng cách A vì công cụ ảnh AI thường viết sai dấu tiếng Việt.

## Nguyên tắc thiết kế nên giữ

- **Một thông điệp, một hành động.** Nhiều ưu đãi trên một ảnh thì không ưu đãi nào được nhớ.
- Chữ đọc được ở cỡ ảnh nhỏ trên điện thoại; độ tương phản chữ/nền từ 4.5:1 trở lên; không đặt chữ lên vùng ảnh rối.
- Chừa lề an toàn; không đặt chữ quan trọng sát mép hoặc vào vùng giao diện che (đầu/cuối story, góc ảnh bìa).
- Nhất quán thương hiệu: cùng bảng màu, font, vị trí logo qua các ảnh; làm một bộ 3-5 biến thể (cùng bố cục, đổi tiêu đề/màu) để thử xem mẫu nào hiệu quả.
- Ảnh chạy quảng cáo: tránh quá nhiều chữ, tuân thủ chính sách quảng cáo của nền tảng (không hứa hẹn kết quả không có căn cứ, không so sánh trước/sau gây hiểu lầm).

## Rào chắn

- Chỉ dùng ảnh, logo, font, nhạc **có quyền sử dụng**. Không dùng nhân vật/thương hiệu có bản quyền, không mạo danh thương hiệu khác.
- Không dùng khuôn mặt người thật khi chưa có sự đồng ý; không ghép ảnh người nổi tiếng vào quảng cáo.
- Không làm ảnh sản phẩm sai sự thật (màu, kích thước, công dụng), không bịa giá/khuyến mãi/đánh giá/huy hiệu chứng nhận.
- Không nhờ người dùng dán mật khẩu hay khóa API vào cuộc trò chuyện.

## Bàn giao và kiểm tra cuối

Giao: file ảnh đúng kích thước (PNG hoặc JPG), file mô tả JSON đã dùng (để chỉnh sửa/tái tạo sau), 2-3 biến thể nếu người dùng muốn thử, và một dòng gợi ý dùng ở đâu. Trước khi giao tự hỏi: chữ có đúng chính tả và số điện thoại/giá đúng không? Đọc rõ ở cỡ nhỏ chưa? Có gì trong ảnh không có quyền dùng hoặc gây hiểu nhầm không?
