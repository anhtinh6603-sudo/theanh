# An toàn chữ tiếng Việt

## Chuẩn mã hóa

- Lưu HTML, Markdown, JSON và phụ đề bằng UTF-8.
- Dùng `<meta charset="UTF-8">` trong composition.
- Không chuyển chữ Việt qua shell/code page có thể làm mất dấu.
- Tìm lỗi trước duyệt: `�`, ô vuông, dấu hỏi thay thế và mojibake như `Ã`, `Æ`, `áº`, `á»`.

## Font

- Chỉ dùng font bundled hoặc local đã xác minh có glyph tiếng Việt.
- Chụp frame thử chứa: `Uyên Linh — Trí tuệ nhân tạo — 1,1 nghìn người theo dõi`.
- Nếu font display làm dấu lệch/rơi, đổi sang Montserrat, Inter hoặc Roboto; không giữ font đẹp nhưng lỗi.

## Bố cục

- Headline tối đa 7 từ mỗi cụm, 2–4 dòng; body không dùng `<br>` ép dòng.
- Vùng an toàn tối thiểu 6% mỗi cạnh; phụ đề nằm trên vùng điều khiển Reels/TikTok.
- Dùng max-width và line-height; body không dưới 32 px cho video dọc.
- Không để chữ che mắt, miệng, tay hoặc sản phẩm chính.
- Không đặt hai khối chữ dài cùng một vùng.

## Kiểm tra hai vòng

1. Trước dựng: soát chính tả, dấu câu, tên riêng, số và cách đọc TTS.
2. Sau dựng: chạy `hyperframes check`, snapshot midpoint mọi cảnh, xem contact sheet ở kích thước nhỏ.

Không cho duyệt nếu còn mất dấu, font vuông, mojibake, chữ tràn/cắt, tương phản kém, một từ rơi dòng hoặc phụ đề che chủ thể.
