# Phiếu đề xuất đầu tiên - Công xưởng Subagent v1

Chủ duyệt từng mục (✅ / ❌). Chưa duyệt thì không phát sinh phí, không đăng nhập,
không chia sẻ dữ liệu, không hành động bên ngoài.

## Đã cài (trong phạm vi tự làm, hoàn tác bằng git)

- Agent Tổng: `.claude/skills/subagent-factory/SKILL.md` (quy trình 7 bước)
- 8 thành phần trong `factory/`; lệnh kiểm tra `scripts/check_factory.sh` → SẴN SÀNG
- Agent con active: `edit-video`, `content-bot` (`.claude/agents/`)
- Thư mục `inbox/` (nhận việc) và `outputs/` (bàn giao), không đưa lên git

## Bắt buộc

- [x] Duyệt phạm vi quyền trong `factory/permissions.yaml` - chủ duyệt 2026-10-21
- [x] Nơi bàn giao: Google Drive, thư mục "Subagent - Ban giao" - đã tạo và tải thử thành công

## Nên có

- [ ] Hồ sơ thương hiệu: giọng viết, màu, logo, font + 1-3 mẫu vàng đã duyệt
- [ ] Bật trigger "lịch" (scheduled task) - chủ chọn giờ chạy, múi giờ Asia/Ho_Chi_Minh
- [ ] API key cho content-bot (Anthropic/OpenAI) - chủ tự nhập vào secret môi trường

## Tùy chọn

- [ ] Agent `cham-soc-khach` (Facebook/Zalo) - cần chủ đăng nhập, khung 08:00-22:00
- [ ] Nền kỹ thuật edit nâng cao: Whisper.cpp (phụ đề tự động), Real-ESRGAN, rembg
- [ ] Trigger "sự kiện" (đơn mới, bình luận mới) - cần kết nối nguồn sự kiện
