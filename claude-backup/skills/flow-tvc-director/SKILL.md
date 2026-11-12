---
name: "flow-tvc-director"
description: Tự mở và điều khiển Google Flow để tạo, kiểm tra, phát và tải TVC quảng cáo điện ảnh không thoại từ avatar, nhân vật và bối cảnh của người dùng; lần đầu hỗ trợ cấu hình project và alias tài sản, sau đó tự truy cập project đã lưu, dùng Omni 1.1 Flash, video dọc 9:16, chất lượng cao nhất, 10 giây, x1, tối đa 2–3 cảnh, ưu tiên thần thái sang trọng, cảm xúc, chuyển động có câu chuyện và gương mặt nhất quán. Dùng khi người dùng gọi $flow-tvc-director, nói “làm TVC”, “mở Flow”, “tạo video bằng avatar” hoặc yêu cầu GPT điều khiển Flow.
---

# Flow TVC Director

Điều khiển giao diện Flow đang đăng nhập để tạo TVC ngắn có nhận diện ổn định. Ưu tiên thao tác thật trong Flow, không chỉ giao prompt.

## Nạp quy chuẩn

- Luôn đọc `references/flow-ui-map.md` trước khi thao tác Flow.
- Luôn đọc `references/tvc-direction.md` trước khi soạn prompt hoặc tạo video.
- Đọc `references/characters.md` khi dùng avatar hoặc nhân vật đã lưu.
- Đọc `references/property-assets.md` khi làm video bất động sản hoặc khi cần tự chọn bối cảnh căn hộ đã lưu.
- Đọc `references/product-assets.md` khi làm video giới thiệu hoặc trải nghiệm sản phẩm đã lưu.
- Luôn đọc `references/operating-playbook.md` để chạy đúng quy trình tự động từ lúc nhận brief tới khi giao đầu ra.
- Luôn đọc `references/user-config.md`. Nếu cấu hình còn trống, chạy onboarding lần đầu và chỉ lưu URL project cùng tên hiển thị của tài sản; không lưu thông tin đăng nhập.
- Nếu người dùng có một skill thương hiệu/nhân vật riêng và gọi đúng tên đó, đọc thêm skill tương ứng trước khi tạo.

## Mặc định đã xác nhận

- Chế độ: Video.
- Loại video mặc định: `Thành phần`, dùng trực tiếp Nhân vật + Bối cảnh để tạo video. Chỉ dùng `Khung hình` khi người dùng yêu cầu rõ.
- Model: Omni 1.1 Flash.
- Tỷ lệ: 9:16.
- Chất lượng: luôn chọn mức cao nhất mà Omni đang cung cấp trong giao diện; tại lần xác nhận 2026-09-07 là 720p. Không tự hạ xuống 360p để tạo nhanh hơn.
- Thời lượng: 10 giây.
- Số đầu ra: x1 cho lượt thử đầu.
- Nhịp dựng: mỗi đầu ra Omni 10 giây gồm 2 cảnh nhỏ là mặc định, tối đa 3 cảnh nhỏ; mỗi cảnh có mốc thời gian, cỡ cảnh và chuyển biến cảm xúc rõ.
- Nhịp truyện: toàn bộ 10 giây phải là một hành động hoàn chỉnh từ mở đầu → phát triển → cao trào → kết thúc; không được hoàn tất hành động hoặc đứng tạo dáng bất động từ giây 8.
- Mỹ thuật: điện ảnh, sang trọng, cảm xúc, đẹp, lịch lãm; chuyển động tinh tế và có chủ đích.
- Cỡ cảnh: ưu tiên cảnh gần cảm xúc; 70–80% thời lượng dùng medium-close/close-up, toàn cảnh chỉ xuất hiện tối đa 1–2 giây để nhận biết bối cảnh.
- Âm thanh: tuyệt đối không thoại, không voice-over, không giọng nói do nhân vật tạo ra.
- Nếu có nhạc: chỉ dùng nhạc được người dùng yêu cầu; nhân vật chỉ nhép môi rất nhẹ theo nhịp, không phát ra lời.

Chỉ thay mặc định khi người dùng yêu cầu rõ hoặc tùy chọn không còn khả dụng trong giao diện hiện tại.

## Quy trình điều khiển

1. Khi skill được gọi, đọc `references/user-config.md`. Nếu có `project_url`, tự mở URL đó. Nếu chưa cấu hình, mở `https://flow.google.com/`, yêu cầu người dùng đăng nhập/chọn hoặc tạo project, rồi ghi URL project và tên project đã xác nhận vào cấu hình. Nếu chưa đăng nhập hoặc cần quyền truy cập, dừng ở màn hình đó và báo người dùng đăng nhập; không xử lý mật khẩu, OTP hoặc khóa bảo mật.
2. Nếu Flow đã mở đúng project, tiếp tục tại trạng thái hiện tại. Chỉ quan sát trước; không tải lại trang nếu có prompt hoặc lựa chọn chưa lưu.
3. Đọc DOM và ảnh chụp giao diện để xác định trạng thái hiện tại. Không dựa vào tọa độ cũ khi có locator theo tên.
4. Xác định chủ thể bằng alias trong `references/user-config.md` và `references/characters.md`, hoặc dùng tài sản mới người dùng cung cấp.
5. Xác định đúng Nhân vật và bối cảnh thật trong `Hình ảnh`, `Video` hoặc `Tệp tải lên`.
6. Chọn Video → Thành phần → gắn Nhân vật trước, Bối cảnh sau → 9:16 → Omni 1.1 Flash → chất lượng cao nhất hiện có → 10 giây → x1.
7. Soạn prompt theo `references/tvc-direction.md`; tuyên bố bối cảnh đính kèm là không gian bắt buộc và phải hiện rõ trong toàn bộ video. Mặc định chia 10 giây thành 2 cảnh nhỏ, tối đa 3 cảnh nhỏ, có mốc thời gian, hành động liên tục và đường cong cảm xúc; không cắt sang bối cảnh khác.
   Luôn chèn khóa âm thanh: `No dialogue, no speech, no voice-over, no spoken words.`
   Trước khi gửi, chạy cổng an toàn chính sách: trong phần văn bản prompt không ghi tên riêng của nhân vật/người, không dùng `celebrity`, `famous person`, `public figure`, `clone`, `deepfake`, `exact identity`, `exact face` hoặc yêu cầu bắt chước một người thật. Chọn nhân vật bằng component đã gắn và gọi trung tính là `the attached character` hoặc `the woman`.
   Nếu tạo 3 clip/30 giây, phải viết một action continuity sheet trước: clip 1 thiết lập mục tiêu, clip 2 thực hiện hành động chính, clip 3 cho thấy kết quả và hero ending. Mỗi clip nêu rõ trạng thái đầu/cuối và nối logic với clip kế tiếp.
8. Kiểm tra lại đúng các component, prompt, model, tỷ lệ, độ phân giải, thời lượng và số đầu ra trước khi bấm tạo.
   Luôn mở bảng cài đặt và kiểm chứng mức phân giải cao nhất đang khả dụng đã được chọn; không chỉ dựa vào thiết lập từ lượt trước.
9. Bấm tạo khi người dùng đã yêu cầu “tạo”, “tiến hành”, “làm”, “cho xem” hoặc lời tương đương. Không tạo biến thể x2–x4 nếu chưa được yêu cầu.
10. Chờ tác vụ hoàn tất; mở video trong trình chỉnh sửa và phát toàn bộ 10 giây.
11. Kiểm tra nhận diện, bối cảnh, chuyển động, giải phẫu, tính liên tục, câu chuyện hành động và chất điện ảnh theo ba mốc đầu/giữa/cuối. Nếu phát hiện lỗi rõ, không gọi là hoàn thiện; tự viết lại prompt theo nguyên nhân lỗi và tạo lại tối đa một lần trong phạm vi brief. Nếu lần hai vẫn lỗi, báo đúng lỗi và chờ người dùng quyết định.
12. Khi đạt, tự bật video trong trình chỉnh sửa để người dùng xem. Chỉ tải xuống khi người dùng yêu cầu tải/xuất; trả đường dẫn MP4 tuyệt đối nếu đã tải về máy.

## Nguyên tắc nhận diện

- Ưu tiên tài sản nhân vật/avatar đã lưu trong Flow thay vì mô tả lại khuôn mặt bằng chữ.
- Giữ tính liên tục của khuôn mặt, tuổi biểu kiến, màu da, tóc, vóc dáng, trang phục và phụ kiện bằng component đã gắn. Trong prompt chỉ dùng cụm trung tính như `consistent appearance throughout the clip`; không nhấn mạnh sao chép danh tính hay khuôn mặt chính xác.
- Khi ghép cảnh thật, giữ phối cảnh, hướng sáng, điểm tiếp xúc, kích thước tương đối và bóng đổ hợp lý.
- Ảnh bối cảnh đi kèm là nguồn chuẩn tuyệt đối: giữ nguyên kiến trúc, bố cục phòng, bàn, ghế, màn hình, cửa sổ, cây, đèn và các đồ vật nhìn thấy. Không cho mô hình sáng tạo một căn phòng tương tự.
- Không thêm người, sản phẩm, logo, chữ hoặc đạo cụ ngoài brief.
- Nếu avatar và nhân vật cùng xuất hiện, gọi đúng tên từng tài sản và mô tả vị trí/hành động riêng để tránh trộn khuôn mặt.
- Nếu chưa thấy tài sản cần dùng trong Flow, hỏi người dùng tải hoặc chọn lại; không dùng tài sản “gần giống”.

## Cổng chất lượng

- Mặt không trôi, đổi người, méo hoặc thay đổi rõ giữa các cảnh.
- Mắt nhìn có chủ đích; biểu cảm tự nhiên; không cười vô cớ.
- Miệng ổn định, không phát âm hoặc nói; nếu có nhạc thì chỉ nhép rất nhẹ, không há miệng quá rộng.
- Tay, ngón tay, kính, tóc, trang phục và sản phẩm không biến dạng.
- Nhân vật đứng/ngồi/chạm đúng mặt phẳng của cảnh thật; không lơ lửng hoặc xuyên vật thể.
- Đầu ra phải nhận ra ngay là đúng bối cảnh tham chiếu; nếu chỉ là một không gian cùng loại nhưng khác đồ vật, góc nhìn hoặc kiến trúc thì đánh giá là lỗi.
- Ánh sáng và màu da hòa với bối cảnh; không có viền cắt ghép giả.
- Hai hoặc ba cảnh có cùng người, trang phục, đạo cụ và hướng nghệ thuật.
- Chuyển động máy quay êm; không zoom số đơn điệu, rung hoặc cắt giật.
- Không có chữ rác, watermark hoặc logo tự sinh.
- Không có thoại, lời nói, voice-over hoặc âm thanh môi miệng giống đang phát ngôn.
- Prompt không chứa tên người thật/tên nhân vật, cụm từ ám chỉ người nổi tiếng, deepfake, bắt chước hoặc sao chép danh tính.
- Độ phân giải đầu ra là mức cao nhất hiện có của Omni; nếu Flow cung cấp mức cao hơn 720p trong tương lai thì tự động chọn mức cao hơn đó.
- Độ nét cảm nhận phải đạt: mắt, đường nét khuôn mặt, tóc, vải trang phục và vật tương tác rõ; không chấp nhận haze, soft-focus, noise nặng hoặc motion blur trên mặt dù UI ghi 720p.
- Áp dụng khóa trang phục đã được từng người dùng xác nhận trong `references/user-config.md`; nếu chưa có khóa, không tự suy đoán trang phục mặc định.
- Không mở đầu bằng cảnh toàn thân xa hoặc cho avatar đi vào khung hình dài vì dễ làm model tái tạo lại khuôn mặt. Đặt avatar hiện rõ ngay từ khung đầu, ưu tiên medium/medium-close, chuyển động đầu nhỏ và không che mặt.
- Luôn mô tả điểm nhìn, chuyển động mắt và biến đổi cảm xúc cụ thể ở từng cảnh nhỏ; tránh gương mặt trung tính kéo dài hoặc chỉ mô tả hành động cơ học.
- Chuyển động phải có easing mềm, mỗi cảnh một chuyển động máy chính và một hành động nhân vật chính; cắt trên hành động để tránh cảm giác giật hoặc rời rạc.
- Hero ending phải giữ ánh mắt ổn định 1–1,5 giây, dùng micro-expression và tư thế mở để thể hiện sang trọng, thần thái, đẹp, đẳng cấp và lịch lãm.
- Hero ending không phải freeze-frame: chỉ giảm tốc trong 0,5–0,8 giây cuối và vẫn duy trì nhịp thở, chớp mắt, ánh mắt, tóc/vải và camera drift rất nhẹ tới khung hình cuối. Nếu nhân vật dừng hẳn trước giây 9,2 thì đánh giá là lỗi nhịp.
- Luôn thêm tín hiệu sống vừa đủ: nhịp thở, chớp mắt, chuyển trọng lượng, quán tính tóc/vải, điều chỉnh bàn tay và parallax hậu cảnh. Với hai người, phản ứng cảm xúc phải xảy ra nối tiếp thay vì đồng thời.
- Khi kiểm tra đầu ra, xem riêng các mốc 0–2 giây, 4–6 giây và 8–10 giây. Cảnh cuối phải tiếp tục câu chuyện và hoàn tất hành động đúng sát cuối video; không chấp nhận đoạn cuối lặp khung, đứng im hoặc mất động lực chuyển động.

## Mẫu prompt Thành phần đã tạo thành công

Dùng cấu trúc này làm nền, sau đó thay hành động và đạo cụ theo brief:

`Create one continuous 10-second vertical cinematic shot. The attached environment is the mandatory physical location and must remain clearly recognizable throughout the entire video. Place the attached fictional character naturally in that exact environment. Preserve the architecture, visible furniture, objects, lighting fixtures, camera side and perspective from the attached environment. Do not invent, redesign, replace, simplify or move to another location. Begin on a wide-medium view that clearly establishes the real environment, then use a slow controlled 50mm dolly-in. The character performs one subtle purposeful action, then slowly shifts her gaze toward the camera and lifts her chin slightly with calm, luxurious confidence. Keep the same location and camera axis from beginning to end. Realistic scale, contact shadows, matching light direction, natural skin, stable hands and anatomy. No cuts, no scene transition, no new location, no extra people, no new objects, no text, no logo, no camera shake. No dialogue, no speech, no voice-over, no spoken words. Mouth stays naturally closed.`

## Xử lý cảnh báo chính sách

- Không cam kết prompt “không bao giờ” bị chặn vì Flow tự quyết định bộ lọc; mục tiêu là giảm tối đa lỗi chặn nhầm bằng cách viết đúng chính sách.
- Nếu Flow báo liên quan người nổi tiếng, không bấm `Thử lại` với nguyên văn prompt cũ.
- Dùng `Sử dụng lại câu lệnh`, giữ component hợp lệ, rồi viết lại trung tính: bỏ toàn bộ tên riêng và cụm khóa danh tính; chỉ mô tả bối cảnh, hành động, máy quay, ánh sáng và tính liên tục hình ảnh.
- Không tìm cách lách hoặc vô hiệu hóa bộ lọc. Nếu bản trung tính vẫn bị chặn, dừng tạo và đề nghị dùng một nhân vật hư cấu/ảnh người dùng có quyền sử dụng khác.

## Ghi nhớ và cập nhật

Xem `references/characters.md` là sổ alias tài sản Flow. Khi người dùng xác nhận thêm avatar/nhân vật lâu dài, bổ sung đúng tên hiển thị và project đã kiểm chứng; không lưu mật khẩu, cookie, API key hoặc dữ liệu đăng nhập.

Nếu Flow đổi giao diện hoặc thêm model/tính năng, cập nhật `references/flow-ui-map.md` bằng quan sát thực tế trước khi sửa quy trình.
