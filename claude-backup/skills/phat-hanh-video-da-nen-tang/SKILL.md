---
name: "phat-hanh-video-da-nen-tang"
description: "Nhận video MP4 người dùng đã duyệt (thường từ skill Flow dựng phim tự động), nghiên cứu xu hướng và chính sách hiện hành của TikTok, Facebook, YouTube, viết bộ tiêu đề, caption, hashtag, CTA và bình luận điều hướng riêng cho từng nền tảng, xin xác nhận rồi đăng và kiểm tra bài bằng đúng tài khoản người dùng qua trình duyệt. Dùng khi người dùng muốn đăng video vừa làm, phát hành phim ngắn lên nhiều nền tảng, viết caption đăng video, hoặc kiểm tra bài đã đăng."
---

# Phát hành video đa nền tảng

Nhân viên phát hành đứng sau **flow-dung-phim-tu-dong**: nhận đúng video người dùng đã xem và duyệt, nghiên cứu thị trường, viết nội dung riêng từng nền tảng, kiểm tra chính sách, rồi đăng qua giao diện hiện hành.

Mục tiêu là tăng khả năng được đề xuất và chuyển đổi bằng sự liên quan, nguyên bản, hook rõ, metadata tốt và CTA hợp lý. Không hứa "lên xu hướng".

## 1. Quy tắc cốt lõi

- **Xác nhận ngay trước khi đăng.** Mọi lần bấm Đăng / Publish / Lên lịch / gửi bình luận / ghim đều cần người dùng xác nhận **tại thời điểm đó**, sau khi xem bản cuối. Câu "ok" khi duyệt video, hay lời dặn "tự động hết" từ đầu, không thay được xác nhận này.
- **Chỉ báo những gì thật sự xảy ra.** Không nói "đã đăng" khi mới lưu nháp hoặc chưa mở được bài thật.
- **Lỗi là dừng.** Đăng nhập, quyền, CAPTCHA, lỗi chính sách hay lỗi xử lý: dừng nền tảng đó, báo nguyên văn lỗi, giữ nguyên kết quả các nền tảng khác.
- **Không đăng trùng.** Bài đã đăng thành công không được đăng lại chỉ vì người dùng nói "tiếp tục".
- **Không đụng vào thông tin đăng nhập.** Không nhập email, mật khẩu, OTP, CAPTCHA; không lấy cookie/token; không tạo hoặc mua tài khoản; không đổi quyền quản trị.
- Không tự chạy quảng cáo, chia sẻ sang nhóm/tin, xóa hay sửa bài sau đăng ngoài phạm vi đã xác nhận.

## 2. Điều kiện bắt đầu

Chỉ chuẩn bị phát hành khi:
- file MP4 cuối tồn tại và mở được;
- người dùng đã xem và nói rõ video đạt;
- đã biết nền tảng đích: TikTok, Facebook (trang cá nhân hoặc fanpage nào), YouTube;
- biết thị trường và ngôn ngữ (mặc định Việt Nam, tiếng Việt nếu hợp brief);
- nếu có bình luận điều hướng: người dùng đã nêu mục đích và đưa **URL thật**.

Chỉ một câu "OK" ngay sau khi gửi video, ngữ cảnh rõ ràng: coi là duyệt video để **soạn kế hoạch**, chưa phải xác nhận đăng.

Không lấy video từ dự án khác, không tự chọn bản nháp cũ, không trộn caption hay link của dự án khác.

## 3. Nhận bàn giao và chống đăng trùng

Thư mục dự án:

```text
outputs/<slug>/
|-- <slug>-final.mp4
|-- publication-handoff.json     do khâu Flow tạo
`-- publish/
    |-- publication-plan.json
    `-- publication-log.json
```

- Đọc `publication-handoff.json` mới nhất của cuộc trò chuyện này; chưa có mà video vừa tạo rõ ràng thì tự lập. Cập nhật `user_video_approval` thành `approved` kèm câu duyệt của người dùng.
- `rights_status`: không tự suy ra `user_confirmed` chỉ vì video do AI tạo. Chưa rõ quyền hình ảnh, nhạc, tài sản bên thứ ba thì giữ `unknown` và hỏi trước khi đăng.
- Tính SHA-256 của video (`sha256sum`), đối chiếu `publication-log.json`. Cặp video + nền tảng + tài khoản đã `posted` thì không đăng lại.
- Kiểm tra video: âm thanh, tỷ lệ, ảnh bìa, chữ nằm trong vùng an toàn, các khẳng định có thể gây hiểu nhầm.

## 4. Nghiên cứu xu hướng và chính sách

Làm riêng cho từng nền tảng và thị trường, tại thời điểm đăng:
1. Xác định chủ đề, thể loại, mâu thuẫn, cảm xúc, khán giả, lời hứa của video.
2. Thu tín hiệu mới: xu hướng, từ khóa tìm kiếm, video tương tự, câu hỏi lặp lại trong bình luận. Ưu tiên nguồn chính thức: TikTok Creative Center (lọc Việt Nam), tìm kiếm trên chính nền tảng, YouTube Search/Autocomplete và Research tab nếu có, Reels/Search và insight của Page trên Facebook.
3. Ghi nguồn, khu vực, ngày kiểm tra. Lượt dùng lớn nhưng đang đi xuống hoặc dữ liệu cũ thì không gọi là "đang viral". Trend của TikTok không mặc định hợp với Facebook hay YouTube.
4. Không tìm được dữ liệu tin cậy: vẫn viết bằng từ khóa liên quan và ghi `trend_research.status: "unverified"`. Không bịa thứ hạng hay độ hot.

Phân tích hook đối thủ: ghi lại kiểu hook, không chép câu chữ.

Kiểm tra chính sách (đọc lại nguồn chính thức khi cần, vì chính sách thay đổi):
- TikTok Community Guidelines và điều kiện đề xuất For You: tiktok.com/community-guidelines
- Facebook Community Standards: facebook.com/help
- YouTube Community Guidelines, spam, external links, hashtags: support.google.com/youtube

Checklist chung: người dùng có quyền với video, giọng, nhạc, logo; không lộ dữ liệu cá nhân, bôi nhọ, thù ghét, lừa đảo; khẳng định về sức khỏe, tài chính, pháp lý, tin tức đã kiểm chứng; hook/tiêu đề/thumbnail đúng nội dung; hashtag liên quan; CTA không spam, không thao túng tương tác; link mở đúng nơi; có tài trợ hoặc affiliate thì bật nhãn quảng cáo/hợp tác; video AI trông như người thật hoặc sự kiện thật thì bật nhãn nội dung AI/chỉnh sửa khi nền tảng yêu cầu; chọn đối tượng, Made for Kids, giới hạn tuổi theo nội dung thật. Mục nào chưa rõ và có thể dẫn tới gỡ bài hay cảnh cáo: `policy_check: "needs_input"` và hỏi người dùng; không đăng thử.

## 5. Viết nội dung từng nền tảng

Không dán một caption cho mọi nơi. Mỗi đích có: hook (tiêu đề hoặc dòng đầu), caption/mô tả, từ khóa và hashtag, CTA chính, một câu hỏi gợi bình luận tự nhiên, bình luận điều hướng (nếu có), ảnh bìa đề xuất, chế độ hiển thị/lịch, nhãn AI và nhãn quảng cáo.

Caption đi qua các chức năng: **Hook** (xung đột hoặc câu hỏi cụ thể) → **Bối cảnh** (đủ hiểu nhân vật và cái giá) → **Căng thẳng** (gợi điều sẽ chứng kiến) → **Giữ payoff** (không spoil cú lật, không nói quá) → **CTA** (một hành động chính) → **Khám phá** (từ khóa, hashtag).

- **TikTok**: caption gọn, hook + một CTA; hashtag ít nhưng sát; không hứa "link ở bio" nếu chưa có.
- **Facebook**: caption kể chuyện dài hơn được, gợi thảo luận bằng câu hỏi đạo đức/cảm xúc thật; đúng Page hay trang cá nhân; link điều hướng thường đặt ở bình luận.
- **YouTube**: tiêu đề cụ thể có từ khóa chính; dòng đầu mô tả nói đúng video, CTA và link xuống dưới; hashtag liên quan, không nhồi; Shorts có thể không bấm được link trong mô tả/bình luận.

Không dùng mồi tương tác kiểu "comment 1 để nhận", quà không có thật, số liệu bịa, chứng thực giả, khan hiếm giả. Bình luận điều hướng chỉ dùng đúng URL người dùng đưa; kiểm tra link mở đúng nơi; không để chỗ trống kiểu `<URL>`, `[LINK]`, "LINK ZALO".

Lưu vào `publish/publication-plan.json`:

```json
{
  "schema_version": 1,
  "project_slug": "me-chong-giu-vang-cuoi",
  "video_path": "../me-chong-giu-vang-cuoi-final.mp4",
  "video_sha256": "…",
  "user_video_approved": true,
  "market": "VN",
  "language": "vi",
  "trend_research": {"checked_at": "ISO-8601", "sources": [], "status": "verified|unverified", "notes": ""},
  "destinations": [
    {"platform": "tiktok", "account_name": "", "account_url": "", "visibility": "public",
     "publish_mode": "now", "scheduled_at": null, "title": "", "caption": "", "hashtags": [],
     "first_comment": "", "comment_url": "", "pin_comment": false, "cover_path": null,
     "synthetic_media_disclosure": "required|not_required|unknown",
     "branded_content_disclosure": "required|not_required|unknown",
     "policy_check": "passed|blocked|needs_input", "final_confirmation": "pending"}
  ]
}
```

Nếu skill có `scripts/validate_publication_plan.py`: chạy `python3 <đường-dẫn-skill>/scripts/validate_publication_plan.py publish/publication-plan.json --draft` sau khi soạn, và chạy lại **không có** `--draft` trước khi xin xác nhận đăng. `video_path` tính từ thư mục `publish/` (vì vậy là `../<slug>-final.mp4`) và không được ra ngoài thư mục dự án. Kết quả `INVALID` thì sửa trước khi đi tiếp.

## 6. Mở nền tảng và kiểm tra tài khoản

- Website đi qua trình duyệt. Dùng trình duyệt người dùng ưu tiên (trình duyệt tích hợp hoặc Chrome) và **đọc skill của trình duyệt đó trước**.
- Mỗi nền tảng: mở trang đăng/quản lý chính thức (TikTok Studio, Meta Business Suite hoặc Facebook, YouTube Studio), kiểm tra tài khoản, kênh, fanpage đang hoạt động. Nút Theo dõi/Nhắn tin không chứng minh quyền quản trị fanpage.
- Chưa đăng nhập hoặc sai tài khoản: dừng và nhờ người dùng tự đăng nhập trên cửa sổ đang mở, rồi báo "đã đăng nhập". Sau đó quan sát lại tên/handle/URL và quyền đăng.
- Quan sát rồi mới thao tác, sau đó quan sát lại; không dùng vị trí nút nhớ từ lần trước.

## 7. Bản nháp và xác nhận

Được phép mở trình đăng, tải đúng video và điền nháp khi người dùng đã yêu cầu đăng. Kiểm tra trên nháp: tài khoản; chế độ hiển thị và lịch; tiêu đề, caption, hashtag; ảnh bìa và khung cắt; đối tượng/Made for Kids; bình luận, remix, duet, tải xuống; nhãn AI và nhãn quảng cáo; cảnh báo bản quyền âm thanh. Không bật quảng cáo trả phí, tự chia sẻ, nhóm/tin ngoài kế hoạch.

Trước lần bấm đầu tiên:
1. Gửi người dùng bản xem trước cuối theo từng nền tảng: tài khoản đích, hiển thị/lịch, tiêu đề/caption, hashtag, CTA, bình luận và link, nhãn AI/quảng cáo, ảnh bìa, cùng 2–4 tín hiệu xu hướng đã dùng.
2. Nêu rõ hành động sắp làm, ví dụ: "Đăng công khai lên 3 tài khoản và gửi 3 bình luận điều hướng".
3. Hỏi một câu xác nhận. Một lần xác nhận có thể bao cả loạt nếu đã liệt kê chính xác mọi đích và nội dung.

Nội dung, link, tài khoản, chế độ hiển thị hoặc lịch thay đổi sau khi xác nhận: trình lại phần đổi và xác nhận lại. Chưa xác nhận thì giữ nháp và dừng.

## 8. Đăng, bình luận, kiểm tra

Sau khi được xác nhận, đặt `final_confirmation: "confirmed"` rồi:
- đăng **lần lượt** từng nền tảng, đúng tài khoản và nội dung đã duyệt;
- chờ xử lý nhưng không chờ quá 60 giây một lần; timeout thì kiểm tra thư viện nội dung trước khi thử lại (timeout không có nghĩa là thất bại);
- mở bài thật, kiểm tra video phát được, caption, hashtag, hiển thị, ảnh bìa đúng;
- gửi bình luận đã duyệt đúng bài và đúng danh tính, kiểm tra đã hiện; ghim nếu đã được duyệt và có chức năng;
- ghi ngay vào `publish/publication-log.json` sau mỗi bước thành công: `platform`, `account_name`, `video_sha256`, `caption_sha256`, `posted_at`, `post_url`, `post_id`, `comment_status`, `comment_url`, `pin_status`, `status`, `error`;
- video đăng được nhưng bình luận lỗi: ghi `partial_comments`, lần sau chỉ bổ sung bình luận, không đăng lại video.

Không lưu mật khẩu, cookie, token, OTP vào plan hay log.

## 9. Bàn giao

Trả bảng ngắn theo nền tảng: tài khoản, trạng thái, link bài, trạng thái bình luận/ghim, lỗi còn lại. Chỉ ghi "đã đăng" khi đã mở được bài thật.

## Cách gọi mẫu

`Video vừa dựng đạt rồi. Đăng lên TikTok, Facebook (fanpage …) và YouTube. Thị trường Việt Nam. Bình luận điều hướng về nhóm Zalo: https://zalo.me/g/… Nghiên cứu trend, viết nội dung riêng từng nền tảng, cho tôi duyệt bản cuối rồi đăng.`