# Phạm vi hỗ trợ

| Nền tảng | Nhận Skill | Chạy Python/FFmpeg | Điều khiển Flow trên máy người dùng | Kết quả khả dụng |
|---|---:|---:|---:|---|
| Claude Code / Desktop có local tools | Có | Có | Có nếu trình duyệt được cấp quyền | Toàn bộ MP4 |
| Codex desktop/CLI | Có | Có | Có nếu trình duyệt được cấp quyền | Toàn bộ MP4 |
| Gemini CLI | Qua extension | Có | Tùy môi trường | Toàn bộ hoặc bộ bàn giao |
| Cursor Agent | Qua project rule | Có | Tùy môi trường | Toàn bộ hoặc bộ bàn giao |
| Claude web/mobile và chat cloud | Qua Project/attachment | Không mặc định | Không truy cập máy cá nhân | Kịch bản + prompt + timeline + phụ đề |

Một file ZIP không thể tự cấp quyền truy cập trình duyệt, tài khoản Flow, API key hay máy tính cá nhân. Agent phải nói đúng năng lực thực tế của môi trường và bàn giao bước còn lại, không giả vờ đã tạo/tải/xuất video.
