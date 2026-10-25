# CLAUDE.md

## Đội agent / skill nội dung (SUBAGENT_HQ)

Repo này có 20 agent (Claude Skill) đang vận hành cho kênh Phong Menly — AI Go
Global, đăng ký đầy đủ tại `SUBAGENT_HQ/config/registry.json`.

**Quy tắc bắt buộc — không ngoại lệ:** mỗi khi giao việc cho một agent nằm
trong `registry.json` (viết bài, trả lời comment, SEO, tạo ảnh/video, chạy
quảng cáo...), phải đi qua vòng đời `hq.py` trước khi coi là xong:

```
hq.py new <agent> <input> "<mô tả>"   # nhận việc, chống trùng
hq.py check <job_id> <hành_động>      # kiểm tầng quyền — dừng nếu tier ≥ 3 mà chưa xin duyệt
hq.py run <job_id>                     # đánh dấu đang làm (agent thật chạy qua Skill/Agent tool)
hq.py gate <job_id> <tiêu_chí> pass|fail "<bằng chứng>"   # đủ 6 tiêu chí mới được đóng job
hq.py done <job_id>
```

Không gọi skill trực tiếp cho các việc có ảnh hưởng công khai (đăng bài, gửi
tin, trả phí, xuất bản) mà bỏ qua `hq.py check` — đây là lớp kiểm quyền duy
nhất đảm bảo không có gì được đăng/gửi mà chưa qua đúng tầng duyệt.

Agent mới luôn thêm bằng `hq.py add-agent` (tự động `status: draft`, không
nhận job). Chỉ `hq.py activate <agent>` sau khi đã test ổn. Không sửa tay
`status` trong `registry.json` để bỏ qua bước này.

Chi tiết đầy đủ: [SUBAGENT_HQ/README.md](SUBAGENT_HQ/README.md).
