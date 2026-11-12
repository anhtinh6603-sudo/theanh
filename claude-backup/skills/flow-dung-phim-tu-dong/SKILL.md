---
name: "flow-dung-phim-tu-dong"
description: "Nhận flow-manifest từ skill Đạo diễn triệu view, tự đưa ảnh nhận dạng nhân vật, ảnh cảnh và chỉ dẫn chuyển động vào Google Flow qua trình duyệt, tạo clip từng cảnh theo thứ tự, kiểm tra nhận dạng, ghép trong Scenebuilder, tải MP4 hoàn chỉnh và gửi lại cho người dùng; có lưu trạng thái để làm tiếp khi bị gián đoạn. Dùng khi người dùng muốn dựng video từ kịch bản và ảnh trên Google Flow, nói dựng phim, làm tiếp phim đang dựng, xem phim dựng tới đâu, hoặc dựng lại một cảnh."
---

# Flow dựng phim tự động

Nhân viên sản xuất đứng sau **dao-dien-trieu-view**: nhận gói bàn giao, vận hành Google Flow qua trình duyệt, dựng từng clip, ghép, tải MP4 và gửi cho người dùng. Khâu sau là **phat-hanh-video-da-nen-tang**.

Google Flow tiêu tốn credit của tài khoản người dùng. Việc người dùng yêu cầu dựng video bằng skill này là đồng ý tải **đúng các tài sản trong manifest** lên Flow và tạo clip trong giới hạn bên dưới. Không tạo hoặc mua tài khoản, không mua credit, không đổi gói, không đăng hay chia sẻ công khai.

## 1. Quy tắc cốt lõi (học từ DramaClaw)

1. **Bước tiếp theo luôn lấy từ trạng thái, không đoán.** Mỗi lần được gọi, đọc `flow-run-state.json` trước rồi mới quyết định làm gì (xem mục 3).
2. **Lỗi là dừng.** Flow báo lỗi, hết credit, từ chối prompt, mất đăng nhập, upload hỏng: dừng ngay, ghi trạng thái, báo người dùng **nguyên văn thông báo lỗi** và việc họ cần làm. Không thử nút khác, không đổi model, không nghĩ ra cách vòng.
3. **Chỉ báo những gì thật sự xong.** Không nói "đã dựng xong" khi mới có clip rời. Không nói cảnh đã đạt khi chưa xem lại clip.
4. **Mỗi thời điểm chỉ một việc tốn credit.** Tạo xong một cảnh, kiểm tra, ghi trạng thái, rồi mới sang cảnh tiếp. Không bấm Generate hàng loạt.
5. **Nhận dạng nhân vật là ưu tiên số một.** Mặt, tóc, trang phục phải khớp ảnh nhận dạng (`identity_ref`). Clip đổi mặt nhân vật là clip hỏng, dù đẹp đến đâu.
6. **Không xóa, không ghi đè.** Không xóa clip, dự án hay tài sản cũ trên Flow. Làm lại toàn bộ dự án cần người dùng xác nhận hai lần (lần 1: có muốn làm lại không; lần 2: nói rõ run state và clip đã chọn sẽ bị thay, credit sẽ tốn lại).

## 2. Nhận đầu vào

Ưu tiên `outputs/<slug>/flow-handoff/flow-manifest.json` mới nhất của **chính cuộc trò chuyện này**. Không lấy tài sản từ dự án khác. Nhiều gói đều có thể là "mới nhất" thì hỏi người dùng chọn.

Manifest dùng schema 2 do Đạo diễn triệu view tạo (vẫn chấp nhận schema 1 cũ, không có `characters`). Các trường chính: `project.slug`, `target` (tỷ lệ, tổng thời lượng), `characters[]` (`id` NVxx, `identity_ref`, `locked_traits`, `voice`), `locations[]`, `props[]`, `scenes[]` (`id` C001…, `order`, `desired_duration_seconds`, `generation_mode` = `frames` | `start_frame` | `ingredients` | `text`, `cast`, `start_image`, `end_image`, `ingredients`, `motion_prompt`, `dialogue[]`, `audio_direction`, `trim_in`, `trim_out`, `status`), `assembly` (`scene_order`, `final_filename`).

Chưa có manifest nhưng kịch bản, ảnh, thứ tự cảnh trong cuộc trò chuyện đã rõ: tự lập manifest theo đúng schema đó. Chỉ hỏi khi thiếu ảnh bắt buộc, thứ tự cảnh hoặc thời lượng.

**Tiền kiểm manifest** (chạy trước khi mở Flow):
- Nếu skill có `scripts/validate_manifest.py`: chạy `python3 <đường-dẫn-skill>/scripts/validate_manifest.py <manifest>`. Kết quả `INVALID` thì dừng và báo lỗi cho người dùng; `WARNING` thì đọc và xử lý nếu ảnh hưởng nhận dạng.
- Không có script thì tự kiểm: mọi file tồn tại; mã cảnh và `order` không trùng, liên tục từ 1; `scene_order` khớp thứ tự; tổng `desired_duration_seconds` lệch mục tiêu không quá 1 giây; cảnh không phải `text` có `start_image`; mọi mã trong `cast` có trong `characters` và có `identity_ref`.
- Chỉ cảnh `status: "approved"` được tạo. Cảnh `draft` bỏ qua và báo lại.

## 3. Trạng thái và bước tiếp theo

`flow-handoff/flow-run-state.json`:

```json
{
  "manifest_sha256": "…",
  "flow_project_name": "DDTV-…",
  "started_at": "ISO-8601",
  "credit_budget": {"max_generations_per_scene": 2},
  "scenes": {
    "C001": {"status": "completed", "attempts": 1, "selected_flow_asset": "C001-v1",
             "identity_check": "passed", "added_to_scene": true, "notes": ""}
  },
  "final": {"status": "pending", "path": null}
}
```

Trạng thái cảnh chỉ gồm: `pending`, `generating`, `completed`, `failed`, `blocked`, `needs_redo`.

Cập nhật run state **ngay sau mỗi hành động có tác dụng bên ngoài** (upload, generate, chọn clip, thêm vào scene, tải về).

Run state chỉ dùng lại khi `manifest_sha256` khớp manifest hiện tại. Manifest đã đổi: so sánh từng cảnh, chỉ đánh dấu `needs_redo` cho cảnh có nội dung khác; không coi mọi clip cũ đều hỏng, cũng không coi mọi clip cũ đều còn dùng được.

**Xác định bước tiếp theo** theo thứ tự:
1. Còn cảnh `generating` → mở Flow, kiểm tra clip đó đã ra chưa (không bấm Generate lại).
2. Còn cảnh `pending` hoặc `needs_redo` (theo `order`) → tạo cảnh đó.
3. Mọi cảnh `completed` nhưng chưa ghép → ghép trong Scenebuilder.
4. Đã ghép nhưng chưa có file cuối → tải về và bàn giao.
5. `final.status = completed` → báo đã xong, gửi lại file nếu cần.

Khi người dùng hỏi "dựng tới đâu rồi": đọc run state và trả bảng ngắn (đã xong / đang tạo / còn lại / lỗi), cùng bước tiếp theo. Không mở Flow chỉ để trả lời câu hỏi này, trừ khi có cảnh đang `generating`.

## 4. Mở Google Flow

- Website đi qua trình duyệt, không qua điều khiển máy tính. Dùng trình duyệt người dùng ưu tiên (trình duyệt tích hợp hoặc Chrome) và **đọc skill của trình duyệt đó trước** (built-in-browser hoặc chrome-browser).
- Mở `https://labs.google/fx/tools/flow`. Kiểm tra đã đăng nhập đúng tài khoản có quyền dùng Flow.
- Chưa đăng nhập, sai tài khoản hoặc phiên hết hạn: dừng tại màn hình đó và nói: *"Google Flow chưa được đăng nhập. Anh/chị đăng nhập tài khoản Google Flow trên cửa sổ đang mở rồi báo tôi 'đã đăng nhập' để tôi làm tiếp."* Không nhập email, mật khẩu, OTP, không động vào trình quản lý mật khẩu.
- CAPTCHA, xác minh tuổi, cảnh báo bảo mật: dừng để người dùng tự xử lý.
- Mở dự án theo `flow_project_name`, hoặc tạo dự án mới tên rõ ràng (`DDTV-<slug>`). Không ghi đè dự án cũ.
- Đọc model, tỷ lệ, thời lượng clip và mức credit đang hiển thị. Chọn theo giao diện hiện tại; không giả định tên model hay vị trí nút từ lần trước.

## 5. Tạo clip từng cảnh

Xử lý theo `order`, **một cảnh một lúc**:

1. Quan sát giao diện trước mỗi thao tác. UI đổi thì đọc lại nhãn, không bấm mù theo tọa độ cũ.
2. Chọn chế độ theo cảnh và khả năng Flow đang hiển thị:
   - Ảnh đầu + ảnh cuối → Frames (start + end): dùng khi cần kết đúng bố cục hoặc match cut.
   - Ảnh đầu + nhân vật cần giữ → Ingredients/references nếu có, đưa `identity_ref` của **mọi nhân vật trong `cast`** + ảnh bối cảnh/đạo cụ. Nếu Flow không cho dùng cùng lúc ảnh đầu và references, ưu tiên ảnh đầu (đã được tạo từ ảnh nhận dạng) và nhắc lại `locked_traits` trong prompt.
   - Chỉ ảnh đầu → animate từ start frame.
   - `text` → text-to-video, chỉ khi manifest chủ đích như vậy.
3. Chỉ tải lên đúng file liệt kê cho cảnh đó. Không tải cả thư mục hay file khác.
4. Prompt = `motion_prompt` + ràng buộc nhận dạng (tóm tắt `locked_traits` của từng nhân vật trong cảnh) + thoại nếu model hỗ trợ âm thanh. Cấu trúc: `[chủ thể + hành động] + [biểu cảm, nhịp] + [máy quay] + [thay đổi ánh sáng/môi trường] + [điểm kết thúc] + [phải giữ nguyên] + [âm thanh/thoại]`. Thoại tiếng Việt: ghi nguyên câu trong ngoặc kép, ghi rõ ai nói và giọng theo trường `voice` của nhân vật, để giọng một nhân vật nhất quán qua các cảnh.
5. Tỷ lệ theo dự án, **1 output mỗi lần**, thời lượng là mốc Flow hỗ trợ gần nhất nhưng không ngắn hơn nội dung bắt buộc (phần dư cắt khi ghép).
6. Đặt `status: generating`, ghi run state, rồi bấm Generate. Chờ bằng các lần chờ ngắn; quá 60 giây thì báo tiến độ ngắn cho người dùng.
7. **Xem lại clip** và kiểm tra:
   - **Nhận dạng**: mặt, tóc, trang phục của từng nhân vật khớp ảnh nhận dạng; không đổi giữa đầu và cuối clip.
   - Hành động chính, hướng nhìn đúng kịch bản; đạo cụ quan trọng còn đó.
   - Không lỗi hình thể (tay, ngón, mặt méo), chữ hoặc logo lạ.
   - Khung cuối nối được với cảnh sau.
   - Thoại (nếu tạo native) không sai nội dung nghiêm trọng, đúng người nói.
8. Đạt: đặt tên theo mã cảnh (`C001-v1`), thêm vào Scene, ghi `completed` + `identity_check: passed`.

**Ngân sách credit**: mặc định 1 lần tạo + tối đa 1 lần làm lại mỗi cảnh. Chỉ làm lại khi có lỗi phá truyện: **sai nhận dạng**, hành động ngược, mặt biến dạng, vật chứng biến mất, chữ/logo lạ nổi bật. Lỗi thẩm mỹ nhỏ không đáng tốn credit. Làm lại thì sửa đúng nguyên nhân trong prompt (ví dụ thêm ràng buộc khuôn mặt, giảm chuyển động máy), không viết lại toàn bộ. Hai lần đều chưa ổn: chọn bản dùng được nhất, ghi chú lỗi, đi tiếp. Riêng lỗi **sai nhận dạng nhân vật chính** sau 2 lần: đặt `blocked` và hỏi người dùng (dùng tạm, sửa ảnh khung đầu, hay cho thêm credit) thay vì tự đi tiếp.

## 6. Ghép video

- Dùng Scenebuilder của Flow làm phương án chính.
- Thêm đúng một clip đã chọn cho mỗi mã cảnh, xếp theo `assembly.scene_order`.
- Cắt đầu/cuối theo `trim_in`, `trim_out` hoặc `desired_duration_seconds`.
- Xem các điểm nối trước, rồi xem toàn bộ: thiếu cảnh, trùng cảnh, khung giật, nhảy nhận dạng giữa hai cảnh liền nhau, âm lượng đột biến, tổng thời lượng.
- Lỗi chỉ sửa được bằng đổi clip: quay lại đúng cảnh đó, không làm lại cả dự án.
- Tải scene hoàn chỉnh dưới dạng video. Xác định đúng file vừa tải bằng tên và thời gian; không lấy đại "file mới nhất" khi có nhiều file.
- Chỉ dùng công cụ hậu kỳ khác (ví dụ ffmpeg, skill video-editing) khi manifest có lớp bắt buộc mà Scenebuilder không làm được (phụ đề cứng, nhạc riêng); vẫn giữ thứ tự và timing của manifest.

## 7. Bàn giao

- Lưu file cuối vào `outputs/<slug>/<slug>-final.mp4`. Nếu máy người dùng đang kết nối và họ chỉ định thư mục, chép thêm vào đó.
- Kiểm tra trước khi báo xong: file tồn tại, dung lượng lớn hơn 0, là video (không phải GIF hay ảnh bìa); dùng `ffprobe` (nếu có) để lấy thời lượng thật; số cảnh và thứ tự khớp manifest.
- Ghi `final.status: completed` và đường dẫn vào run state.
- Tạo `outputs/<slug>/publication-handoff.json` cho khâu phát hành: `schema_version: 1`, `project_slug`, `title`, `video_path` (tên file MP4), `video_sha256`, `language`, `story_summary`, `hook`, `target_audience`, `source_manifest`, `synthetic_or_altered_media: true`, `rights_status: "unknown"` (chỉ đổi thành `user_confirmed` khi người dùng xác nhận quyền), `user_video_approval: {"status": "awaiting"}`.
- **Gửi file MP4 cho người dùng** (gửi file, không chỉ đưa đường dẫn). Kèm một dòng: số cảnh, thời lượng thực tế, số lần làm lại, cảnh nào còn lệch đáng chú ý.
- Hỏi người dùng xem và duyệt video. Khi họ duyệt và muốn đăng, chuyển sang skill **phat-hanh-video-da-nen-tang**.

## 8. Dựng lại một cảnh

Khi người dùng muốn sửa một cảnh đã dựng, thứ tự cố định:
1. Cập nhật manifest trước (prompt, thoại, ảnh). Nếu đổi thoại hoặc hình, việc này thuộc khâu đạo diễn: sửa kịch bản và ảnh trước.
2. Đặt cảnh đó `needs_redo` trong run state.
3. Tạo lại đúng cảnh đó (tính vào ngân sách credit).
4. Thay clip trong Scenebuilder, ghép lại và tải bản mới với tên `<slug>-final-v2.mp4` (không ghi đè bản cũ).

Không bỏ qua bước 1 để dựng lại luôn, và không dựng lại cả phim khi chỉ một cảnh đổi.

## 9. Phục hồi

- **Mất phiên/tab**: mở lại đúng dự án theo `flow_project_name`, đối chiếu clip theo mã cảnh và run state.
- **Generate không rõ kết quả (timeout)**: kiểm tra thư viện dự án trước; không bấm Generate lần nữa chỉ vì chờ lâu.
- **Clip đã tạo nhưng run state chưa ghi**: nhận diện clip theo mã, prompt, thời gian rồi ghi bổ sung; không tạo lại.
- **Upload lỗi**: kiểm tra file và định dạng, thử lại 1 lần. Không thay bằng ảnh khác ngoài manifest.
- **Lỗi chính sách nội dung**: báo nguyên văn; đề xuất chỉnh prompt cho tuân thủ, không tìm cách lách bộ lọc.
- **Hết credit, tính năng không có ở tài khoản/khu vực**: dừng, báo chính xác bao nhiêu cảnh xong, còn lại cảnh nào.
- **Scenebuilder sai thứ tự**: so toàn bộ dãy mã với `scene_order`, sửa, xem lại.

## Cách gọi mẫu

- `Dựng phim trên Flow từ gói đạo diễn vừa tạo, trả MP4 cho tôi.`
- `Phim mẹ chồng dựng tới đâu rồi?`
- `Làm tiếp phim đang dựng.`
- `Dựng lại cảnh C004, nhân vật bị đổi mặt.`