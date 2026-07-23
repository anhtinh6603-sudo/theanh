# Content Bot System — 6 bot tự động hoá content

Hệ thống 6 bot nối tiếp nhau, lấy cảm hứng từ pipeline "6 Bot trong hệ thống"
(Nhật Dương). Mỗi bot là 1 script Python độc lập, giao tiếp với nhau qua file
(`data/*.jsonl` + markdown frontmatter) — chạy rời từng bot hay chạy cả chuỗi
qua cron đều được.

```
Bot 1 Web Scraper  → data/trending.jsonl
Bot 2 Ideator       → data/ideas.jsonl
Bot 3 Writer        → data/drafts/*.md   (markdown + YAML frontmatter)
Bot 4 Image Gen     → data/images/*.png  (cập nhật frontmatter)
Bot 5 Video Render  → data/videos/*.mp4  (cập nhật frontmatter)
Bot 6 Auto-poster   → đăng lên platform cấu hình, log data/published.jsonl
```

## Bot 1 — Web Scraper

Cào tin trending từ RSS (báo) + Hacker News + Reddit (JSON công khai). **Không**
cào trực tiếp Facebook/TikTok: hai nền tảng này chặn scraping tự động ở tầng
mạng lẫn ToS (đã tự kiểm chứng: bị chặn ngay ở bước kết nối), nên RSS + API
công khai là lựa chọn ổn định và hợp lệ hơn để lấy tín hiệu "đang hot".

## Bot 2 — Ideator

Đưa tin thô cho Claude/OpenAI, yêu cầu chọn ra góc độ (angle) khác biệt, dễ
viral. Có cơ chế tránh lặp: `data/used_topics.json` lưu các angle đã dùng gần
đây và được đưa lại vào prompt để model không viết lại chủ đề cũ.

## Bot 3 — Writer

Viết bài đầy đủ (blog chuẩn SEO hoặc social caption) từ mỗi idea, lưu thành
file markdown có YAML frontmatter (title, meta_description, social_caption,
hashtags, status...).

## Bot 4 — Image Gen

Trích 1 prompt tiếng Anh từ bài viết, gọi API sinh ảnh. Hỗ trợ OpenAI
(`gpt-image-1`) hoặc Leonardo AI (`IMAGE_PROVIDER` trong `.env`). Không hỗ trợ
Midjourney vì nền tảng này không có API chính thức.

## Bot 5 — Video Render

Chuyển bài viết thành kịch bản 4-8 cảnh (Claude), tạo giọng đọc TTS cho từng
cảnh (mặc định dùng `edge-tts` — miễn phí, có giọng tiếng Việt), rồi dùng
ffmpeg dựng mỗi cảnh (Ken Burns pan/zoom + caption cháy chữ) và ghép lại thành
1 video dọc 1080x1920.

**Yêu cầu**: ffmpeg hệ thống có `libx264` + `libfreetype` + `libfontconfig`
(mặc định đúng với `apt install ffmpeg` / `brew install ffmpeg`).

Đã test bằng ffmpeg thật (không phải ffmpeg.wasm): render nhiều cảnh với
caption tiếng Việt có dấu, ký tự đặc biệt (`:`, `'`, `%`), text tự động
xuống dòng đúng khung hình — output là mp4 h264/aac 1080x1920 hợp lệ.

## Bot 6 — Auto-poster

Tự động đăng bài (upload media + dán caption + bấm publish) đúng khung giờ
vàng (`PUBLISH_WINDOW_START`/`PUBLISH_WINDOW_END` trong `.env`), bằng
Playwright điều khiển browser.

**Quan trọng**:
- Bot **không** lưu hay xử lý mật khẩu của bạn. Nó dùng persistent browser
  profile của Playwright — bạn tự đăng nhập bằng tay 1 lần
  (`python bots/bot6_auto_poster.py --setup`), session được lưu lại trên đĩa
  và các lần chạy sau tái sử dụng session đó, y hệt một trình duyệt không bao
  giờ đóng.
- Hầu hết nền tảng (Facebook, Instagram...) cấm tự động hoá giao diện web
  thường trong Điều khoản dịch vụ, kể cả với tài khoản của chính bạn. Nếu nền
  tảng có API chính thức (Facebook/Instagram Graph API, TikTok Content Posting
  API, REST API của blog...), hãy ưu tiên dùng API — ổn định và đúng ToS hơn.
  Chỉ dùng cách browser-automation này cho nơi không có API, hiểu rõ rủi ro
  ToS/khoá tài khoản, và chỉ trên tài khoản của chính bạn.
- Selector DOM (CSS selector cho ô upload/caption/nút publish) **không được
  đóng sẵn** vì mỗi nền tảng/tài khoản/thời điểm một khác. Copy
  `platforms.example.yaml` thành `platforms.yaml` rồi tự điền selector sau khi
  tự mở devtools kiểm tra trang compose thật của bạn.

## Cài đặt

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium   # chỉ cần nếu dùng Bot 6

cp .env.example .env           # rồi điền API key
cp platforms.example.yaml platforms.yaml   # nếu dùng Bot 6, điền selector thật
```

## Chạy thử

```bash
# chạy toàn bộ pipeline 1 lần
python pipeline.py --all

# chỉ chạy một vài bot
python pipeline.py --only 1,2

# đăng nhập 1 lần cho Bot 6 (mở browser thật, tự đăng nhập bằng tay)
python bots/bot6_auto_poster.py --setup --platform my_blog
```

## Chạy định kỳ (cron)

Xem `scripts/crontab.example` — bot 1-5 chạy mỗi vài giờ để tích luỹ nội
dung, Bot 6 chạy mỗi 15 phút và tự no-op ngoài khung giờ vàng.

## Giới hạn đã biết

- Bot 1 dùng RSS/HN/Reddit thay vì cào trực tiếp mạng xã hội (xem lý do ở
  trên).
- Bot 5 hiện dùng lại 1 ảnh (từ Bot 4) cho mọi cảnh, chỉ đổi cách pan/zoom —
  chưa sinh ảnh riêng cho từng cảnh.
- `edge-tts` (TTS miễn phí mặc định) cần kết nối ra ngoài tới máy chủ
  Microsoft; một số mạng doanh nghiệp/proxy có thể chặn — nếu vậy, đổi
  `TTS_PROVIDER=openai` trong `.env`.
- Bot 6 chỉ có khung (engine) tổng quát; bạn phải tự điền selector thật cho
  nền tảng mình dùng trong `platforms.yaml`.
