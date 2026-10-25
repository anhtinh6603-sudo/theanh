# SUBAGENT_HQ — Đầu não điều phối đội agent

Khung ghi nhận job, kiểm quyền và quality gate cho đội agent (hiện là các
Claude Skill: `content-research-ideas`, `facebook-content-phong-menly`,
`youtube-video-full-seo`, v.v. — xem đủ danh sách trong `config/registry.json`).

**hq.py không tự chạy agent.** Nó chỉ là xương sống bookkeeping: mọi việc đi
qua đăng ký (ai được làm gì), kiểm quyền (4 tầng) và quality gate (6 tiêu
chí) trước khi coi là "xong". Việc thực thi thật vẫn do Claude gọi đúng
Skill/Agent tool khi được giao.

## Đội agent hiện tại

`config/registry.json` có đúng 20 agent, chọn từ các Claude Skill thật đang
có trong tài khoản (research, content, thiết kế, video, CSKH, quảng cáo/hạ
tầng). Nếu đội quân thật của bạn khác, sửa lại `name`/`capability`/`actions`
trực tiếp trong file, hoặc dùng lệnh dưới để thêm/mở agent đúng quy trình.

## Thêm agent mới — luôn qua draft trước

```bash
# Thêm — luôn tạo ở status=draft, KHÔNG nhận job ngay
python3 hq.py add-agent "<ten_agent>" "<nhom>" "<nang_luc>" "draft,post"

# Test ổn rồi mới cho chạy thật
python3 hq.py activate <ten_agent>
```

Không sửa tay `"status"` trong `registry.json` để bỏ qua bước test — luôn
đi qua `add-agent` → `activate`.

## Vòng đời 1 job

```bash
# 1. Nhận việc — chống trùng theo hash(agent + nội dung)
python3 hq.py new facebook-content-phong-menly "mô tả hoặc đường dẫn file" "Viết bài X"

# 2. Kiểm quyền cho từng hành động job cần làm
python3 hq.py check <job_id> draft    # tier 1 → exit 0, tự động
python3 hq.py check <job_id> post     # tier 3 → exit 2, phải xin duyệt chủ trước khi đăng

# 3. Giao agent con làm (đánh dấu running — việc thật làm bên ngoài hq.py)
python3 hq.py run <job_id>

# 4. Theo dõi
python3 hq.py status
python3 hq.py status <job_id>

# 5. Quality gate — đủ 6 tiêu chí mới đóng được job
python3 hq.py gate <job_id> yeu_cau      pass "đúng yêu cầu gốc"
python3 hq.py gate <job_id> thuong_hieu  pass "đúng văn phong kênh"
python3 hq.py gate <job_id> ky_thuat     pass "không lỗi chính tả/định dạng"
python3 hq.py gate <job_id> quyen        pass "đúng tầng quyền, có xin duyệt"
python3 hq.py gate <job_id> trai_nghiem  pass "đọc tự nhiên, không sáo ngữ"
python3 hq.py gate <job_id> bang_chung   pass "link bài/preview/log đính kèm"

# 6. Nếu agent làm sai: ghi lý do, tối đa 2 lần, hết lượt thì status=blocked
python3 hq.py retry <job_id> "văn phong chưa đúng, agent viết quá dài"

# 7. Đóng job khi đủ gate
python3 hq.py done <job_id>
```

## Khóa agent / dừng khẩn

```bash
python3 hq.py lock <agent_name>   # khóa 1 agent, nó không nhận job mới nữa
python3 hq.py activate <agent_name>  # mở lại agent (draft hoặc locked) -> active
python3 hq.py stop                # DỪNG KHẨN toàn bộ — xoá SUBAGENT_HQ/jobs/HALT để mở lại
```

## 4 tầng quyền (config/permissions.json)

| Tầng | Ý nghĩa | Ai quyết |
|---|---|---|
| 1 | Tự động hoàn toàn | Agent tự làm |
| 2 | Tự động có giám sát | Agent làm, hiện tiến trình |
| 3 | Xin duyệt trước bước cuối | Chủ duyệt rồi agent mới bấm nút cuối |
| 4 | Chủ trực tiếp thao tác | Agent không được chạm — đăng nhập/OTP/thanh toán |

`hq.py check` tự tính tầng theo hành động (`draft`, `post`, `publish`,
`send_message`, `pay`, `login`...) khai trong `action_tiers` — không tính
thủ công, không đoán.

## Nguyên tắc cứng

- Không lưu/hiển thị mật khẩu, OTP, API key, token, cookie, thông tin thanh toán trong `jobs/jobs.json` hay `logs/hq.log.jsonl`.
- Không agent nào tự mở rộng quyền — mọi nâng cấp phải qua `status: draft` → test → chủ duyệt → `"active"`.
- Chỉ nói "xong" khi `hq.py done` chạy thành công (đủ 6 gate, không có gate fail).
