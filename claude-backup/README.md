# Sao lưu dữ liệu Claude

Ngày sao lưu: 2026-11-12. Gồm:

- `skills/` - 42 skill riêng của tài khoản (đã cài qua plugin trên claude.ai). Không gồm 13 skill mặc định của Anthropic (pdf, docx, xlsx, pptx, docs, ...), vì chúng luôn có sẵn.
- Công xưởng Subagent: `../.claude/skills/subagent-factory/` và các agent con trong `../.claude/agents/`.
- Hệ 6 bot: `../.claude/skills/content-bot-system/` và `../content-bot-system/`.

Cài lại một skill: nén thư mục skill thành .zip rồi tải lên claude.ai (Settings → Capabilities → Skills), hoặc chép vào `.claude/skills/` của một dự án Claude Code.

| Skill | Mô tả | Cập nhật |
|---|---|---|
| `ai-bao-cao-kinh-doanh` | Tổng hợp báo cáo kinh doanh - doanh thu, số đơn, số khách/lead, chi phí quảng cáo và hiệu quả từng kênh (CPA, CPL, ROAS, tỷ lệ chốt, lợi nhu… | 2026-09-19 |
| `ai-nghien-cuu-thi-truong` | Nghiên cứu thị trường để quyết định bán gì, cho ai, cạnh tranh thế nào - tìm nhu cầu, xác định khách hàng mục tiêu, phân tích đối thủ (giá, … | 2026-09-19 |
| `ai-thiet-ke-quang-cao` | Thiết kế hình ảnh marketing - ảnh quảng cáo Facebook/Instagram, poster, thumbnail YouTube, banner web, cover fanpage, story dọc, ảnh giới th… | 2026-09-19 |
| `biet-doi-content-ai-5-phut` | Tạo trọn gói content marketing đa nền tảng bằng quy trình 5 mô-đun liên hoàn gồm nghiên cứu ý tưởng, viết nội dung, thiết kế concept hình ản… | 2026-09-19 |
| `bo-ai-marketing` | Bộ AI Marketing bán hàng gồm 10 mô-đun - Nghiên cứu thị trường, Content, Thiết kế, Video, Fanpage Chatbot, Zalo CSKH, Website và Landing Pag… | 2026-09-19 |
| `chuyen-video-tinh-thanh-dong` | Biến một hoặc nhiều ảnh tĩnh thành video dọc có chuyển động, giữ nhận diện nhân vật và sản phẩm, sau đó ghép cảnh, đồng bộ lời thoại, làm ph… | 2026-09-19 |
| `content-research-ideas` | Nghiên cứu chủ đề/trend và lên danh sách ý tưởng nội dung cụ thể cho kênh Facebook/YouTube "Phong Menly AI Go Global". Dùng khi chủ kênh cần… | 2026-09-26 |
| `dao-dien-trieu-view` | Đạo diễn phim ngắn AI - biến chủ đề hoặc kịch bản có sẵn cùng thời lượng thành gói sản xuất video hoàn chỉnh (ý tưởng, kịch bản theo timecod… | 2026-10-05 |
| `dau-nao-subagent` | Agent Tổng Giám Sát điều phối công xưởng Subagent: nhận việc, kiểm quyền, giao agent con, quality gate, bàn giao. Dùng khi gọi Đầu não/Agent… | 2026-09-28 |
| `doi-agent-tong-chi-huy` | Điều phối đội agent cá nhân: Tổng chỉ huy chia mục tiêu kinh doanh thành việc nhỏ, giao 10 agent chuyên môn (nghiên cứu, nội dung, video, Yo… | 2026-09-26 |
| `edit-captioned-vertical-video` | Edit existing footage into polished captioned vertical videos with fixed or adapted on-screen text, music, darkening or blur, slow motion, c… | 2026-09-19 |
| `edit-dang-1-thoai-thumbnail` | Edit Dạng 1: video talking-head dọc 9:16 cắt gọn tự nhiên + thumbnail tiêu đề mở đầu + caption động theo lời nói. Dùng khi khách nói "edit D… | 2026-10-02 |
| `facebook-comment-natural-reply` | Trả lời hàng loạt bình luận Facebook (fanpage Phong Menly - Ai Go Global US) một cách tự nhiên, đa dạng, không lặp khuôn mẫu — dùng khi Uyên… | 2026-09-26 |
| `facebook-content-phong-menly` | Tạo nội dung Facebook tự nhiên dựa trên kênh mẫu của từng người dùng; phân tích link kênh, tự chọn định dạng, viết bài và nội dung ảnh/carou… | 2026-08-22 |
| `flow-dung-phim-tu-dong` | Nhận flow-manifest từ skill Đạo diễn triệu view, tự đưa ảnh nhận dạng nhân vật, ảnh cảnh và chỉ dẫn chuyển động vào Google Flow qua trình du… | 2026-10-05 |
| `flow-tvc-director` | Tự mở và điều khiển Google Flow để tạo, kiểm tra, phát và tải TVC quảng cáo điện ảnh không thoại từ avatar, nhân vật và bối cảnh của người d… | 2026-09-19 |
| `geminigen-image` | Generate images directly via GeminiGen.ai API and save local files for downstream posting/creative workflows. Use when the user asks to crea… | 2026-09-19 |
| `google-tts-reply` | Generate Vietnamese speech audio from text using Google Cloud Text-to-Speech and prepare it for outbound chat delivery. Use when building or… | 2026-09-19 |
| `hoan-doi-nhan-vat-thuong-hieu` | Hoán đổi nhân vật trong ảnh tham chiếu bằng gương mặt và trang phục thương hiệu cố định của “cô gái áo vàng”, đồng thời bám sát bối cảnh, bố… | 2026-09-19 |
| `huong-dan-edit-video-bang-ai` | Hướng dẫn edit (dựng, chỉnh sửa) video bằng AI - cắt thô theo nội dung, tự động phụ đề tiếng Việt, cắt khoảng lặng, dựng theo bản chép lời, … | 2026-09-19 |
| `huong-dan-lam-video-bang-ai` | Hướng dẫn làm video bằng AI từ đầu đến cuối - lên ý tưởng và kịch bản (hook 3 giây), chia cảnh (shot list), viết prompt tạo ảnh/video AI, gi… | 2026-09-19 |
| `huong-dan-y-tuong-nghien-cuu-viet-content` | Hướng dẫn tìm kiếm ý tưởng, nghiên cứu thị trường và viết content thu hút - xác định chân dung khách hàng và nỗi đau, phân tích đối thủ và k… | 2026-09-19 |
| `kenh-phat-phap` | Dựng nội dung và video ngắn cho kênh Phật pháp tiếng Việt - viết kịch bản 30-45 giây, kiểm định chất lượng nội dung (chặn mê tín, chặn ép tư… | 2026-08-09 |
| `pdf-extract-crop` | Extract text, screenshots, page images, and targeted regions from PDF files. Use when reading PDF catalogs, pulling structured text from PDF… | 2026-09-19 |
| `phat-hanh-video-da-nen-tang` | Nhận video MP4 người dùng đã duyệt (thường từ skill Flow dựng phim tự động), nghiên cứu xu hướng và chính sách hiện hành của TikTok, Faceboo… | 2026-10-05 |
| `social-photo-content-publisher` | Phân tích kênh mạng xã hội hoặc kênh đối thủ, chọn ý tưởng và định dạng, tạo bài ảnh từ ảnh thật, chèn text, viết caption tự nhiên, chọn nhạ… | 2026-09-19 |
| `thuong-hieu-ca-nhan` | Dùng khi người dùng muốn tạo bộ ảnh thương hiệu cá nhân đồng nhất, chèn tiêu đề hoặc badge lên ảnh Facebook/Instagram, hoặc xây dây chuyền x… | 2026-09-19 |
| `thuong-hieu-khach-san-hoa-do` | Bộ nhận diện và quy trình nội dung Khách sạn Hoa Đô: thông tin liên hệ, phong cách poster, giọng văn, caption mẫu, video review hằng ngày. D… | 2026-10-05 |
| `video-editing` | Chỉnh sửa video bằng ffmpeg - cắt/ghép clip, đổi định dạng/nén/đổi độ phân giải, thêm phụ đề hoặc chữ overlay, tách/ghép âm thanh và nhạc nề… | 2026-07-26 |
| `video-editing-2` | Chỉnh sửa video bằng ffmpeg - cắt/ghép clip, đổi định dạng/nén/đổi độ phân giải, thêm phụ đề hoặc chữ overlay, tách/ghép âm thanh và nhạc nề… | 2026-07-26 |
| `video-mmtd` | Tạo hoặc chỉnh sửa video dọc TikTok, Reels và Shorts dành riêng cho sách Mật Mã Tự Do từ ảnh KOL, ảnh bìa sách, lời thoại hoặc video có sẵn;… | 2026-09-19 |
| `videoviral` | Tạo video dọc viral dạng tin tức, review hoặc giới thiệu từ ý tưởng, văn bản hay URL, theo phong cách editorial ấm của video Uyên Linh: hình… | 2026-09-19 |
| `vietnamese-tts-video` | Renders a vertical (9:16) Vietnamese talking-photo/promo video — a real reference photo with AI narration and burned Vietnamese captions — u… | 2026-09-19 |
| `xay-app-phan-mem-tu-dong` | Xây dựng ứng dụng/phần mềm nhỏ tự động hóa công việc (quản lý đơn, khách, kho, đặt phòng, chấm công, báo cáo, công cụ nội bộ) - từ xác định … | 2026-09-19 |
| `xay-chay-quang-cao-tu-dong` | Xây dựng quy trình chạy quảng cáo tự động (Facebook/Meta Ads, TikTok Ads, Google Ads) - tính điểm hòa vốn (CPA, ROAS), thiết kế cấu trúc chi… | 2026-09-19 |
| `xay-fanpage-chatbot-tu-dong` | Xây dựng chatbot tự động cho fanpage Facebook (Messenger) - thiết kế kịch bản hội thoại, bộ câu trả lời mẫu, luồng thu số điện thoại/chốt đơ… | 2026-09-19 |
| `xay-quy-trinh-email-tu-dong` | Xây dựng quy trình email marketing tự động (email chào mừng, nuôi dưỡng khách, giỏ hàng bỏ quên, sau mua, kéo khách cũ, bản tin định kỳ) - g… | 2026-09-19 |
| `xay-trang-ban-hang-tu-dong` | Xây dựng trang bán hàng (landing page/sales page) tự động - từ ưu đãi, cấu trúc trang, nội dung thuyết phục, form đặt hàng, thanh toán/COD/c… | 2026-09-19 |
| `xay-website-tu-dong` | Xây dựng website tự động cho doanh nghiệp/thương hiệu/dịch vụ nhiều trang - từ mục tiêu và sơ đồ trang, chọn nền tảng (WordPress, no-code ho… | 2026-09-19 |
| `xay-zalo-cham-soc-khach-tu-dong` | Xây dựng quy trình chăm sóc khách hàng tự động trên Zalo theo từng giai đoạn (mới quan tâm, tư vấn, chốt đơn, sau mua, tái mua, khách nguội)… | 2026-09-19 |
| `youtube-video-full-seo` | SEO đầy đủ cho 1 video YouTube mới đăng trên kênh Phong Menly AI Go Global (chưa public) — timeline, thẻ (cards), màn hình kết thúc, từ khóa… | 2026-09-26 |
| `zalo-tra-loi-khach` | Soạn tin nhắn trả lời khách hàng, người quen hoặc người đang test bot trên Zalo theo đúng giọng của chủ tài khoản - ngắn, tự nhiên như chat … | 2026-09-19 |
