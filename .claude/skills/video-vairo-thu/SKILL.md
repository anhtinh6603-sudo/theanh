---
name: video-vairo-thu
description: "Tạo trọn gói video dọc hài kịch với nhân vật thú nhân hóa nhất quán: viết kịch bản, tạo ảnh cảnh, làm chuyển động bằng Google Flow, tạo thoại ElevenLabs, burn phụ đề và xuất MP4 đã kiểm tra. Dùng trên Claude Code/Desktop, Codex, Gemini CLI, Cursor hoặc các agent tương thích khi người dùng gọi ‘Video vairo thú’ hay muốn sản xuất TikTok/Reels/Shorts tương tự."
---

# Video vairo thú

Sản xuất video dọc có chuyển động thật, lời thoại, nhạc/SFX, phụ đề cháy và báo cáo kiểm tra. Skill này không phụ thuộc riêng Codex hay Windows; script chính dùng Python 3 và FFmpeg trên Windows, macOS hoặc Linux.

## Kiểm tra năng lực môi trường trước khi làm

- Nếu có quyền đọc/ghi file, chạy lệnh, điều khiển trình duyệt đã đăng nhập Google Flow và có FFmpeg: thực hiện trọn quy trình đến MP4.
- Nếu chỉ ở web/điện thoại hoặc môi trường cloud không truy cập được máy người dùng: vẫn tạo bộ sản xuất gồm kịch bản, storyboard, prompt Flow, `takes.json`, `timeline.json` và phụ đề; nói rõ bước nào cần chuyển sang máy có Flow/FFmpeg. Không tuyên bố đã xuất MP4 khi chưa có file thật.
- Không nhúng API key, cookie, mật khẩu hoặc dữ liệu đăng nhập vào dự án/Skill. Chỉ đọc khóa từ biến môi trường và không in khóa ra log.

## Đầu vào tối thiểu

- Ý tưởng hoặc chủ đề; nếu thiếu, tự đề xuất một tình huống hài gia đình an toàn.
- Ảnh nhận diện nhân vật hoặc mô tả nhân vật cố định.
- Thời lượng mục tiêu, mặc định 35–45 giây.
- Quyền dùng Google Flow và cấu hình giọng ElevenLabs của người vận hành.

## Quy trình bắt buộc

1. Tạo thư mục dự án bằng `python scripts/new_video_project.py --project <duong-dan> --title <ten>` hoặc theo [references/project-contract.md](references/project-contract.md).
2. Viết hook, thoại và storyboard theo [references/creative-system.md](references/creative-system.md). Câu chuyện phải có mở nút, leo thang và punchline.
3. Tạo một ảnh khóa cho mỗi cảnh. Giữ cast bible, quần áo, tỉ lệ cơ thể, đạo cụ và bối cảnh ổn định. Ảnh nguồn không có chữ, logo hoặc watermark.
4. Tạo chuyển động từng ảnh trong Google Flow theo [references/flow-production.md](references/flow-production.md). Xác nhận chi phí tín dụng trước thao tác tiêu tín dụng nếu người dùng chưa duyệt rõ số lượng hoặc ngân sách.
5. Tải từng MP4 gốc, đặt tên `flow/scene-01.mp4`, `scene-02.mp4`… rồi xem khung đầu–giữa–cuối.
6. Tạo từng câu thoại bằng ElevenLabs theo [references/elevenlabs-audio.md](references/elevenlabs-audio.md), ưu tiên một file mỗi lượt thoại và timing thật trong `timeline.json`.
7. Viết phụ đề ASS từ timing thật. Mỗi nhịp 2–5 từ, ở vùng an toàn phía dưới, không che mặt hay đạo cụ.
8. Dựng bằng `python scripts/render_video.py --project <duong-dan>`, rồi chạy `python scripts/qc_video.py --video <duong-dan-final.mp4>`. Sửa và chạy lại tới khi đạt chuẩn.
9. Trả MP4 bằng đường dẫn tuyệt đối, kèm thời lượng, độ phân giải và kết quả QC.

Các file PowerShell trong `scripts/` chỉ là tiện ích tương thích ngược cho Windows; quy trình chuẩn dùng file `.py`.

## Chuẩn hình ảnh và chuyển động

- Mặc định 1080×1920, 30 fps, H.264, `yuv420p`, AAC 48 kHz, `faststart`.
- Một ảnh khóa tương ứng một cảnh. Với clip Flow 8 giây, cắt theo nhịp kịch bản; tổng thời lượng phải đúng mục tiêu.
- Prompt chuyển động chỉ mô tả 1–3 hành động rõ, chuyển động máy nhẹ và các bất biến cần giữ.
- Luôn ghi: không thoại, không lip-sync, không thêm nhân vật, không chữ, không logo, không watermark.
- Nếu Flow làm hỏng nhận diện, chi, đạo cụ hoặc thêm chữ, tạo lại đúng cảnh đó.

## Chuẩn âm thanh và phụ đề

- Không ghép một đoạn thoại dài rồi đoán thời gian; tạo từng lượt thoại để đặt chính xác.
- Nhạc nền thấp hơn thoại rõ rệt; SFX chỉ nhấn hành động.
- Mức tham chiếu cuối khoảng −15 LUFS, true peak không cao hơn −1.5 dBFS.
- Burn phụ đề vào pixel và kiểm tra dấu tiếng Việt sau render.

## Cổng kiểm duyệt

Chỉ giao bản final khi đủ cảnh, đúng thứ tự/thời lượng; nhận diện ổn định; không có khung đen, file hỏng hoặc đứng hình bất thường; thoại dễ nghe; phụ đề khớp; `ffprobe` xác nhận H.264/AAC, 1080×1920, 30 fps; giải mã toàn bộ không lỗi; và contact sheet đã được xem bằng mắt.

Đọc [references/post-production-qa.md](references/post-production-qa.md) khi dựng hoặc xử lý lỗi. Đọc [PLATFORM-SUPPORT.md](PLATFORM-SUPPORT.md) nếu môi trường không có đủ công cụ để hoàn tất video.
