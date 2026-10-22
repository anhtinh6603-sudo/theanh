# Phiếu đề xuất - Công xưởng Subagent

Cập nhật 2026-10-22. Chủ đã duyệt toàn bộ ("cài hết").

## Bắt buộc - XONG

- [x] Phạm vi quyền `factory/permissions.yaml` - duyệt 2026-10-21
- [x] Bàn giao: Google Drive "Subagent - Ban giao"

## Nên có

- [x] Mẫu hồ sơ thương hiệu `factory/memory/brand.md` - **chờ chủ điền/gửi mẫu**
- [x] Lịch sáng 07:37 (Asia/Ho_Chi_Minh): cài lại công cụ, kiểm hệ thống, quét Drive "Subagent - Nhan viec"
- [ ] API key cho content-bot - **chủ tự thêm** vào cài đặt môi trường (biến `ANTHROPIC_API_KEY` hoặc `OPENAI_API_KEY`). Thư viện của content-bot đã cài.

## Tùy chọn

- [x] Agent `cham-soc-khach` - đã tạo, chỉ soạn nháp; **chờ chủ kết nối kênh** Facebook/Zalo
- [x] rembg (xóa nền) - cài và chạy thử đạt
- [~] Whisper.cpp - đã build; **model bị chặn** vì mạng môi trường chưa cho phép `huggingface.co`
- [x] Real-ESRGAN - chủ cho phép 2026-10-22; chạy thử 320x240 → 1280x960 đạt
- [~] Kích hoạt theo sự kiện - file mới trên Drive bắt qua lịch sáng; đơn/bình luận cần kết nối kênh
