# Workflow dựng Video MMTD

## Media

Ưu tiên: media người dùng cung cấp; bộ Mật Mã Tự Do trong Google Drive; sau cùng là media mới được người dùng chấp thuận. Không dựa vào tên file để kết luận, phải xem ảnh trước khi dựng.

Bộ 5 cảnh gợi ý:

1. Brand hero — KOL cầm sách, dùng cho hook.
2. Founder tại bàn — vấn đề đổi thời gian lấy tiền.
3. Product spotlight — giới thiệu cuốn sách.
4. Desk flatlay — tiền, thời gian và lựa chọn.
5. Lifestyle reading — suy ngẫm và CTA.

## Nội dung

- Hook 0–2 giây bằng câu hỏi gây suy nghĩ.
- Mỗi cảnh chỉ mang một ý.
- Không tuyên bố người nói đã trải nghiệm điều không có bằng chứng.
- Viết chính xác “Mật Mã Tự Do”.
- CTA của series chỉ dùng khi brief yêu cầu: “Comment TỰ DO”.

## Hình ảnh

- 1080×1920, 30 fps, yuv420p.
- Scale cover rồi crop; ưu tiên giữ mặt và bìa sách.
- Push-in 1.00→1.06 trong toàn cảnh.
- 5 cảnh khoảng 6–7 giây; fade khoảng 0,7 giây.
- Màu than #242321, kem #FFF9EE, vàng #E6B93F.
- Không dùng hiệu ứng làm bìa sách khó đọc.

## Voice và caption

Với Edge TTS:

    python scripts/edge_tts_wordtiming.py --text-file SCRIPT.txt --voice vi-VN-NamMinhNeural --rate +8% --audio voice.mp3 --timing word-timing.json
    python scripts/build_karaoke_ass.py --timing word-timing.json --out karaoke.ass

Caption dùng cụm 2–5 từ, word-boundary từ chính audio/TTS, chữ kem, từ đang đọc màu vàng, outline than và nằm trên vùng điều khiển TikTok/Reels.

## Audio

- High-pass khoảng 80 Hz, low-pass khoảng 11 kHz khi phù hợp.
- Loudness mục tiêu khoảng -14 LUFS; true peak không vượt -1,5 dB.
- Fade đầu/cuối ngắn.
- Nhạc nền chỉ thêm khi có nguồn hợp lệ và phải thấp hơn lời đọc.

## Hồ sơ dự án

Tạo BRIEF.md, STORYBOARD.md, SCRIPT.md và media ledger có đường dẫn local, nguồn, loại và cảnh sử dụng.

