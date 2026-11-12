# Kiểm tra chất lượng

## Nội dung

- Hook xuất hiện trong 2 giây đầu.
- Mọi số liệu, tên riêng và tuyên bố quan trọng đều có nguồn.
- Không có câu đọc dài hơn thời lượng cảnh.
- Kết luận trả lời đúng lời hứa của hook.

## Hình ảnh

- Có cả ảnh thật và video thật; tối thiểu 70% thời lượng hình ảnh là media thật liên quan trực tiếp.
- Ảnh/video đã tải về local và có credit.
- Chủ thể không bị crop mất mặt; chữ không chạm biên.
- Contact sheet không có cảnh đen, media đóng băng ngoài chủ ý hoặc nội dung quá nhỏ.

## Chữ tiếng Việt

- File dùng UTF-8 và composition có `<meta charset="UTF-8">`.
- Không có `�`, ký tự vuông, mojibake, mất dấu hoặc dấu tách khỏi chữ.
- Font đã thử với câu tiếng Việt có đủ dấu.
- Headline, body và phụ đề không tràn, không bị cắt và không che chủ thể.
- Đã xem midpoint của từng cảnh ở kích thước điện thoại.

## Âm thanh

- Lời dẫn rõ, phát âm đúng tên riêng và không bị cắt cuối câu.
- Nhạc nền thấp hơn lời dẫn và fade đầu/cuối.
- Phụ đề khớp ý lời nói, nằm trong vùng an toàn và đọc được trên điện thoại.
- Giọng đọc là tài sản thay thế độc lập; có thể đổi voice mà không dựng lại hình.

## Kỹ thuật

- `hyperframes check` không có lỗi chặn render.
- Root có kích thước, `data-start` và `data-duration` chính xác.
- Media có id ổn định, timing hợp lệ và được framework quản lý.
- MP4 có hình, âm thanh, dung lượng khác 0 và thời lượng nằm trong ±0,25 giây so với yêu cầu.
- Hiển thị video bằng đường dẫn tuyệt đối trong câu trả lời cuối.
