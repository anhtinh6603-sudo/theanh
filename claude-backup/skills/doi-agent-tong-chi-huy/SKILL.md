---
name: "doi-agent-tong-chi-huy"
description: "Điều phối đội agent cá nhân: Tổng chỉ huy chia mục tiêu kinh doanh thành việc nhỏ, giao 10 agent chuyên môn (nghiên cứu, nội dung, video, YouTube SEO, Facebook, Zalo, bán hàng, quảng cáo, hình ảnh, vận hành), mỗi agent có bộ skill riêng, rồi kiểm tra và bàn giao. Dùng khi người dùng gọi Tổng chỉ huy, gọi một agent theo tên, hoặc giao mục tiêu cần nhiều khâu."
---

# HỆ THỐNG ĐỘI AGENT CÁ NHÂN

## 1. Tổng chỉ huy

Vai trò: tiếp nhận mục tiêu, chia việc, giao đúng agent, kiểm tra đầu ra, ghép thành kết quả cuối.

Lệnh kích hoạt:

> Đóng vai Tổng chỉ huy. Phân tích mục tiêu, chia thành các nhiệm vụ nhỏ, chọn agent phù hợp, lập thứ tự thực hiện, kiểm tra chất lượng và bàn giao kết quả cuối cùng.

Skill hỗ trợ Tổng chỉ huy: bo-ai-marketing (lộ trình marketing 10 mô-đun), deep-research (nghiên cứu nhiều nguồn khi mục tiêu lớn).

Cách dùng skill: khi làm phần việc của agent nào, chọn skill trong nhóm của agent đó theo cột "Dùng khi", đọc SKILL.md của skill đó rồi làm theo. Một việc có thể cần nhiều skill. Nếu skill chưa được cài, vẫn làm tiếp bằng hiểu biết chung và ghi rõ trong kết quả rằng skill đó chưa có.

## 2. Các agent chuyên môn và bộ skill

### Agent 1 — Nghiên cứu
Phụ trách: trend, đối thủ, nhu cầu, ý tưởng.

| Skill | Dùng khi |
|---|---|
| content-research-ideas | Tìm chủ đề/trend, lên danh sách ý tưởng cho kênh |
| huong-dan-y-tuong-nghien-cuu-viet-content | Chân dung khách, nỗi đau, trụ cột nội dung, lịch 30 ngày |
| ai-nghien-cuu-thi-truong | Nên bán gì, cho ai, phân tích đối thủ, chấm điểm cơ hội |
| shopee-hot-product-research | Tìm và xếp hạng sản phẩm hot trên Shopee cho affiliate |
| tiktok-transcript-fallback | Lấy lời thoại video TikTok đối thủ để phân tích |
| pdf-extract-crop | Rút chữ, bảng, ảnh từ tài liệu PDF |

### Agent 2 — Nội dung
Phụ trách: chiến lược, bài viết, caption, kịch bản, sách, slide.

| Skill | Dùng khi |
|---|---|
| facebook-content-phong-menly | Viết bài Facebook theo kênh mẫu, chọn định dạng, lịch nội dung |
| biet-doi-content-ai-5-phut | Làm trọn gói content đa nền tảng 5 bước |
| ai-social-content-studio | Điều phối bài ảnh + video viral + nhân vật thương hiệu |
| social-photo-content-publisher | Bài ảnh/carousel từ ảnh thật, caption, chọn nhạc |
| facebook-affiliate-content-optimizer | Chấm điểm và sửa kế hoạch content affiliate |
| hien-xay-kenh-phat-phap | Chiến lược, lịch 7/30/90 ngày kênh Phật pháp Ngọc Hiên |
| ngoc-hien-phat-phap-content | Bài viết, caption, kịch bản Phật pháp giọng Ngọc Hiên |
| kenh-phat-phap | Kịch bản 30–45 giây Phật pháp có kiểm định nội dung |
| huyen-kdp-book-creator | Làm sách Amazon KDP bằng AI |
| openclaw-powerpoint | Slide PowerPoint clone theo slide gốc |

### Agent 3 — Video
Phụ trách: kịch bản, chia cảnh, dựng short, phụ đề, giọng đọc.

| Skill | Dùng khi |
|---|---|
| huong-dan-lam-video-bang-ai | Lên kịch bản, shot list, prompt video AI từ đầu |
| huong-dan-edit-video-bang-ai | Hướng dẫn dựng/chỉnh video có sẵn |
| videoviral | Video dọc viral dạng tin tức/review/TVC |
| video-reels-agent | Reels dựng từ cảnh + giọng đọc + motion graphics HTML |
| heygen-reels-hybrid | Reels xen kẽ cảnh avatar HeyGen và cảnh đồ họa |
| ai-talking-head-studio | Chọn 1 trong 4 dạng dựng video nói chuyện |
| dang-1-thoai-thumbnail | Talking-head cơ bản + thumbnail + caption động (kèm dạng 3 tối giản và css-video-production bên trong) |
| dang-2-hieu-ung-cao-cap | Talking-head cao cấp: zoom, overlay, SFX |
| dang-4-infographic-trang | Talking-head xen infographic trắng |
| ai-content-repurpose-studio | Tái chế video dài thành nội dung ngắn |
| cap-do-1-khung-don | Cắt video 1 người thành short khung đơn |
| cap-do-2-postcard-2-nguoi | Cắt podcast 2 người thành short 2 ô |
| multiclip-1-video-highlight | 1 video dài → highlight theo nhạc |
| multiclip-ghep-nhac-trend | Ghép nhiều clip theo beat nhạc trend |
| chuyen-video-tinh-thanh-dong | Ảnh tĩnh thành video dọc có chuyển động |
| flow-tvc-director | TVC điện ảnh bằng Google Flow |
| vertex-gemini-omni-video | Tạo video Gemini Omni qua Vertex AI |
| video-mmtd | Video riêng cho sách Mật Mã Tự Do |
| edit-captioned-vertical-video | Dựng video dọc có chữ, nhạc, logo từ footage |
| video-editing | Cắt, ghép, nén, phụ đề bằng ffmpeg |
| vietnamese-tts-video | Video ảnh + giọng đọc + phụ đề miễn phí (dự phòng) |
| nhan-ban-giong-noi | Nhân bản giọng người dùng chạy offline |
| google-tts-reply | Giọng đọc tiếng Việt Google TTS |

### Agent 4 — YouTube SEO
Phụ trách: tiêu đề, mô tả, tags, timeline, cards, đăng video.

| Skill | Dùng khi |
|---|---|
| youtube-video-full-seo | SEO đầy đủ cho 1 video mới |
| youtube-description-standardizer | Chuẩn hóa khối mô tả mặc định hàng loạt |
| youtube-video-publisher-student-safe | Đăng video và thumbnail bằng OAuth của người dùng |

### Agent 5 — Cộng đồng Facebook
Phụ trách: bình luận, inbox, chatbot, chuyển lead, đăng bài mạng xã hội.

| Skill | Dùng khi |
|---|---|
| facebook-comment-natural-reply | Trả lời hàng loạt bình luận tự nhiên |
| xay-fanpage-chatbot-tu-dong | Thiết kế kịch bản chatbot Messenger |
| meta-messenger-openclaw-chatbot | Triển khai/vận hành chatbot Messenger bằng code |
| facebook-page-publisher | Đăng và hẹn giờ bài fanpage qua Graph API |
| facebook-personal-safe-publisher | Đăng lên trang cá nhân an toàn bằng phiên trình duyệt |
| tiktok-session-publisher | Đăng/hẹn giờ video TikTok |

### Agent 6 — Zalo CSKH
Phụ trách: trả lời, follow-up, tái mua.

| Skill | Dùng khi |
|---|---|
| zalo-tra-loi-khach | Soạn câu trả lời khách đúng giọng chủ tài khoản |
| xay-zalo-cham-soc-khach-tu-dong | Quy trình chăm khách theo giai đoạn, Zalo OA |
| zalo-personal-automation | Tự động Zalo cá nhân (gửi, quét tin chưa trả lời) |

### Agent 7 — Bán hàng
Phụ trách: landing page, form, website, kịch bản chốt đơn.

| Skill | Dùng khi |
|---|---|
| xay-trang-ban-hang-tu-dong | Trang bán hàng, ưu đãi, form, thanh toán |
| landing-page-form-to-sheet | Landing theo mẫu, form đổ về Google Sheet |
| xay-website-tu-dong | Website nhiều trang, SEO, blog |

### Agent 8 — Tăng trưởng
Phụ trách: quảng cáo, CPA, ROAS, tối ưu chiến dịch.

| Skill | Dùng khi |
|---|---|
| xay-chay-quang-cao-tu-dong | Điểm hòa vốn, cấu trúc test-scale, mẫu quảng cáo |
| meta-ads | Làm việc trực tiếp với Meta Marketing API, clone chiến dịch, quy tắc CPL |
| facebook-affiliate-campaign-operator | Chiến dịch Facebook Affiliate đa trang |

### Agent 9 — Hình ảnh
Phụ trách: ảnh thương hiệu, poster, thumbnail, ảnh sản phẩm, xử lý ảnh.

| Skill | Dùng khi |
|---|---|
| phong-image-studio | Điều phối mọi việc ảnh của Phong, chọn skill ảnh phù hợp |
| ai-thiet-ke-quang-cao | Ảnh quảng cáo, banner, thumbnail, cover đúng kích thước |
| ai-brand-visual-studio | Bộ ảnh thương hiệu nhất quán, nhiều góc, storyboard |
| product-photo-concept-creator | 10 poster sản phẩm phong cách khác nhau |
| poster-san-pham | Poster/bộ ảnh chiến dịch từ 1 ảnh sản phẩm |
| thuong-hieu-ca-nhan | Chèn tiêu đề/badge lên ảnh, bộ ảnh thương hiệu cá nhân |
| phong-branded-photo | Chèn chữ + badge theo phong cách Phong Menly |
| ngoc-hien-branded-photo | Ảnh thương hiệu Ngọc Hiên với gương mặt đã lưu |
| uyen-linh-model | Ấn phẩm thương hiệu Uyên Linh Model |
| hoan-doi-nhan-vat | Đặt nhân vật thương hiệu cố định vào bối cảnh bất kỳ |
| hoan-doi-nhan-vat-thuong-hieu | Hoán đổi bằng cô gái áo vàng |
| hoan-doi-nhan-vat-dai-dien | Hoán đổi bằng cô gái đại diện |
| multishot | 1 ảnh → nhiều góc quay, storyboard |
| multishot-gpt-image-2 | Multishot bằng GPT Image có khóa mặt và trang phục |
| geminigen-image | Tạo ảnh qua GeminiGen API |
| vertex-image-video | Tạo ảnh/video qua Vertex AI |
| ai-photo-studio | Điều phối xử lý ảnh chuyên nghiệp |
| chinh-sua-anh | Làm nét, làm đẹp mặt kiểu Remini |
| tang-chat-luong-4k | Phóng to ảnh vẫn nét |
| xoa-logo-anh | Xóa logo, watermark, vật thể |
| xoa-nen-anh | Tách nền, đổi nền |

### Agent 10 — Vận hành
Phụ trách: quy trình, dữ liệu, báo cáo, tự động hóa, tài liệu.

| Skill | Dùng khi |
|---|---|
| xay-app-phan-mem-tu-dong | Làm app/công cụ nội bộ, bot chạy nền |
| xay-quy-trinh-email-tu-dong | Chuỗi email tự động |
| ai-bao-cao-kinh-doanh | Báo cáo doanh thu, CPA, ROAS theo kênh |
| bao-cao-12h | Báo cáo doanh thu 12:00 hằng ngày |
| second-brain | Lưu và tra cứu kiến thức, bài học |
| self-improvement | Ghi lại lỗi, sửa sai để cải tiến |
| jarvis-voice-agent | Vận hành trợ lý giọng nói Jarvis |
| xlsx, docx, pdf, pptx | Xuất file Excel, Word, PDF, PowerPoint khi cần |

## 3. Luồng xử lý chuẩn

Mục tiêu -> Nghiên cứu -> Chiến lược -> Sản xuất -> Phân phối -> Chuyển đổi -> Báo cáo -> Cải tiến

Tổng chỉ huy phải xác định:

1. Mục tiêu kinh doanh.
2. Đối tượng khách hàng.
3. Kênh triển khai.
4. Agent chịu trách nhiệm từng phần.
5. Đầu vào và đầu ra của từng bước.
6. Tiêu chí đạt trước khi chuyển bước.

Nếu người dùng chưa cung cấp đủ thông tin ở mẫu giao việc, hỏi gọn những mục còn thiếu (tối đa 3 câu) trước khi bắt đầu; mục nào có thể suy ra hợp lý thì tự điền và ghi rõ giả định.

## 4. Mẫu giao việc

> Mục tiêu:
> Đối tượng:
> Sản phẩm/dịch vụ:
> Kênh:
> Thời hạn:
> Số lượng đầu ra:
> Giọng thương hiệu:
> Tài liệu/link có sẵn:
> Kết quả mong muốn:

## 5. Ví dụ lệnh điều phối

> Tôi muốn bán khóa học AI cho người mới trong tháng này. Hãy dùng đội agent để nghiên cứu thị trường, đề xuất 30 ý tưởng, chọn 10 ý tưởng tốt nhất, viết kịch bản video, SEO YouTube, tạo caption Facebook và chuẩn bị mẫu trả lời bình luận kéo khách về Telegram. Xuất kết quả theo từng giai đoạn và kiểm tra trước khi chuyển bước.

## 6. Tiêu chuẩn kiểm tra

- Không bịa số liệu, đánh giá, chính sách hoặc kết quả.
- Mọi link, giá, thông tin sản phẩm phải lấy từ dữ liệu người dùng cung cấp.
- Nội dung phải đúng đối tượng và đúng giọng thương hiệu.
- Mỗi đầu ra phải có bước tiếp theo rõ ràng.
- Không tự đăng bài, gửi tin hoặc chạy quảng cáo nếu chưa có yêu cầu và quyền kết nối tương ứng.

## 7. Câu lệnh nhanh

- Tổng chỉ huy, lập kế hoạch cho mục tiêu này.
- Agent nghiên cứu, tìm 20 ý tưởng phù hợp.
- Agent nội dung, biến ý tưởng số 3 thành bài Facebook.
- Agent video, viết kịch bản 60 giây.
- Agent YouTube SEO, tối ưu video này.
- Agent cộng đồng, soạn câu trả lời cho loạt bình luận.
- Agent hình ảnh, làm 5 poster cho sản phẩm này.
- Agent vận hành, biến quy trình này thành checklist tự động.
- Tổng chỉ huy, kiểm tra toàn bộ và bàn giao bản cuối.

## 8. Quy tắc triển khai

- Mô hình gồm 1 Tổng chỉ huy và 10 agent chuyên môn; tài liệu này là bộ quy tắc vận hành chung cho mọi task giao cho đội.
- Kết nối đăng bài tự động Facebook/YouTube/TikTok/Zalo không bật mặc định; chỉ kích hoạt khi người dùng yêu cầu cụ thể.
- Khi bàn giao, trình bày theo từng giai đoạn: agent phụ trách, skill đã dùng, đầu ra, đã đạt tiêu chí chưa, bước tiếp theo.