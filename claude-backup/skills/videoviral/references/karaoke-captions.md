# Phụ đề karaoke mặc định

## Hình thức

- Chỉ dùng phụ đề karaoke trên video thật; không đặt headline, chapter label, data card, khung giá hoặc CTA dạng thẻ nếu người dùng không yêu cầu.
- Chia lời thành cụm 2–5 từ, ưu tiên kết thúc tại dấu câu hoặc ranh giới ý nghĩa.
- Mỗi thời điểm chỉ hiện một cụm. Không để hai cụm chồng nhau ở điểm chuyển.
- Đặt phụ đề ở vùng an toàn phía dưới, chừa giao diện TikTok/Reels; dùng cỡ chữ đủ đọc trên điện thoại.
- Chữ chưa đọc màu trắng kem; từ đang đọc màu vàng `#E6B93F`, có thể scale nhẹ tối đa `1.08`.
- Dùng bóng chữ hoặc gradient tối nhẹ phía dưới để tăng tương phản; không dùng hộp nền lớn.

## Đồng bộ

1. Lấy word timing thật từ TTS có timestamps, forced alignment hoặc transcription word-level. Không chia thời gian đều theo số chữ.
2. Loại token khoảng trắng và ký tự rỗng trước khi chia cụm.
3. Giữ mỗi cụm 2–5 từ; nếu còn một từ lẻ, cân lại cụm trước thành 3+2 hoặc 4+2.
4. Cho cụm kết thúc trước cụm kế tiếp ít nhất `0.02` giây để tránh chồng hình.
5. Tô màu từng từ đúng `start` và trả về trắng tại `end`.

## Kiểm tra

- Chụp snapshot dày tại các điểm chuyển cụm, không chỉ midpoint cảnh.
- Kiểm tra chữ Việt, dấu câu, tên riêng, xuống dòng, vùng an toàn và tương phản.
- Không render nếu còn cụm một từ, cụm quá năm từ, hai dòng chồng nhau hoặc highlight lệch lời rõ rệt.
