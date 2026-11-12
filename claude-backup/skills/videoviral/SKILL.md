---
name: videoviral
description: Tạo video dọc viral dạng tin tức, review hoặc giới thiệu từ ý tưởng, văn bản hay URL, theo phong cách editorial ấm của video Uyên Linh: hình ảnh thật và video thật làm tư liệu chính, tiêu đề tiếng Việt lớn không lỗi, phụ đề rõ, dữ kiện có nguồn, motion graphics nhẹ và tệp MP4. Dùng khi người dùng gọi $videoviral hoặc muốn biến nội dung thành video TikTok, Reels hay Shorts hoàn chỉnh.
---

# Video Viral

Tạo video hoàn chỉnh bằng HyperFrames. Không dừng ở kịch bản hoặc storyboard.

## Mẫu hình ảnh mặc định

Luôn dựng theo `references/golden-style.md`, lấy video lịch sử Uyên Linh làm mẫu vàng. Chỉ đổi phong cách khi người dùng yêu cầu rõ.

## Quy trình bắt buộc

1. Đọc `hyperframes` và đi theo workflow được router chọn. Video nhiều cảnh có lời dẫn thường dùng `general-video`.
2. Đọc `media-use` cho mọi nhu cầu ảnh, video, giọng, nhạc, phụ đề và xử lý media. Đọc các skill HyperFrames theo công đoạn thực tế.
3. Phân tích đầu vào: URL thì đọc nội dung, ngày, tác giả, dữ kiện, ảnh và video nhúng; ý tưởng thì nghiên cứu nguồn chính thức; tệp thì ưu tiên tài liệu người dùng.
4. Chọn cấu trúc tin tức, review hoặc giới thiệu trong `references/formats.md`.
5. Mặc định 1080×1920, 30 fps, tiếng Việt, hook trong 2 giây đầu. Nếu không có thời lượng, dùng 45 giây; 60–90 giây thì chia ba hồi.
6. Viết `BRIEF.md`, `STORYBOARD.md`, `SCRIPT.md` trước khi dựng. Phân biệt dữ kiện, suy luận và đề xuất.
7. Thực hiện cổng media thật trong `references/real-media-policy.md`. Không dựng khi chưa có bộ tư liệu đạt yêu cầu.
8. Tải toàn bộ media cần render về dự án. Không dùng URL mạng làm tài sản render.
9. Dựng theo mẫu vàng về màu, crop và nhịp hình, nhưng mặc định chỉ hiển thị phụ đề karaoke theo `references/karaoke-captions.md`. Không thêm tiêu đề lớn, nhãn chương, khung giá, data card hoặc CTA dạng thẻ nếu người dùng không yêu cầu rõ.
10. Thực hiện cổng chữ tiếng Việt trong `references/text-safety.md` trước và sau khi dựng. Không cho duyệt khi còn chữ lỗi, tràn, che mặt hoặc xuống dòng xấu.
11. Giọng đọc là mô-đun thay thế được. Nếu người dùng cung cấp giọng, ưu tiên giọng đó. Với ElevenLabs, luôn dùng `eleven_v3`; không tự hạ xuống Multilingual v2, Flash hoặc model khác. Chèn audio tag v3 như `[excited]`, `[laughs]`, `[whispers]` hoặc `[sighs]` có chọn lọc theo ngữ cảnh, tối đa 1–2 sắc thái trong một đoạn ngắn để tránh diễn quá mức. Nếu chưa có giọng, dùng giọng tiếng Việt tự nhiên khả dụng và ghi rõ là giọng tạm. Không khóa vào một voice ID hay nhà cung cấp, trừ khi người dùng đã chọn rõ như Adam.
12. Tạo nhạc nền thấp hơn lời đọc. Phụ đề phải dùng word timing thật, chia cụm 2–5 từ cân đối đủ ý và tô vàng đúng từ đang được đọc; không lặp nguyên đoạn dài trên màn hình.
13. Chạy `hyperframes check`; chụp midpoint mỗi cảnh; kiểm tra contact sheet ở kích thước điện thoại. Sửa lỗi chữ, crop, cảnh đen, media đóng băng và sai nguồn.
14. Cho người dùng duyệt contact sheet hoặc preview. Chỉ render khi họ nói “xuất”, “bật”, “cho xem” hoặc đồng ý rõ ràng.
15. Render MP4 chất lượng cao; dùng ffprobe xác minh hình, tiếng, dung lượng và thời lượng; hiển thị video bằng đường dẫn tuyệt đối.

## Hàng rào bắt buộc

- Không thay tư liệu thật bằng hình AI chỉ vì dễ tìm hơn.
- Không dùng ảnh stock chung chung để giả làm nhân vật, sản phẩm, địa điểm hoặc sự kiện cụ thể.
- Không bịa video, số liệu, trích dẫn, trải nghiệm review hay thành tích.
- Không sao chép dài nguyên văn nguồn; diễn đạt lại và ghi nguồn gần dữ kiện.
- Không render nếu `hyperframes check` còn lỗi chặn hoặc contact sheet chưa được xem bằng mắt.
- Không chấp nhận chữ tiếng Việt thiếu dấu, font lỗi dấu, chữ rác, ký tự vuông hoặc dấu tách khỏi chữ.

## Bàn giao

Trả về video phát được, link tải MP4, thời lượng, tỷ lệ, nguồn chính và giọng đã dùng. Mời người dùng gửi voice mới nếu muốn thay giọng mà không phải dựng lại hình.

Đọc `references/golden-style.md`, `references/real-media-policy.md`, `references/text-safety.md`, `references/karaoke-captions.md` trước khi dựng và `references/quality-gates.md` trước duyệt/render.
