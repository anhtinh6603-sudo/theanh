# ElevenLabs và timing thoại

## Bảo mật

- Chỉ lấy API key từ `ELEVENLABS_API_KEY` hoặc biến môi trường được người dùng chỉ định.
- Không đọc khóa từ một dự án khác nếu người dùng chưa cho phép rõ.
- Không in khóa, lưu khóa vào script, JSON, log hoặc gói Skill.

## Cách tạo

1. Chia kịch bản thành từng lượt thoại ngắn; một file MP3 cho mỗi lượt.
2. Khai báo `takes.json` với tên file, biến môi trường voice ID và văn bản.
3. Chạy `scripts/generate-elevenlabs.ps1`.
4. Đo thời lượng thật bằng FFprobe rồi đặt `start_ms` trong `timeline.json`.
5. Nếu lời dài hơn ô thời gian, ưu tiên rút gọn câu hoặc tạo lại take; không tăng tốc quá mức gây méo tiếng.

Model mặc định là `eleven_v3`, ngôn ngữ `vi`. Có thể dùng thẻ cảm xúc ngắn như `[curious]`, `[nervous]`, `[playful]`, nhưng nghe lại từng take vì thẻ có thể được đọc thành lời ở một số giọng/model.

## Cân bằng

- Thoại là lớp ưu tiên.
- Nhạc nền thường ở mức 0.06–0.14 so với toàn thang, tùy bản nhạc.
- SFX ngắn, không che phụ âm đầu câu.
- Mục tiêu final khoảng −15 LUFS; true peak không cao hơn −1.5 dBFS.

