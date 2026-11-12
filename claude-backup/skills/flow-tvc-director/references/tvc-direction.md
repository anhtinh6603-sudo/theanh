# Đạo diễn TVC Omni 10 giây

## Quy tắc nhịp cảnh đã xác nhận

- Mỗi đầu ra Omni 10 giây phải được viết như một sequence quảng cáo hoàn chỉnh gồm 2 cảnh, tối đa 3 cảnh nhỏ có mốc thời gian; không dùng một cú máy kéo dài 10 giây nếu người dùng không yêu cầu riêng.
- Mỗi cảnh nhỏ phải thay đổi cỡ cảnh hoặc vị trí máy có chủ đích: establishing/medium → interaction/detail → emotional hero close-up.
- Cảm xúc phải có đường cong nhìn thấy rõ: tập trung hoặc suy tư → nhận ra/kết nối → tự tin, bình thản ở hero ending. Diễn bằng mắt, lông mày, nhịp thở, cằm, vai và bàn tay; không thoại và không chuyển động miệng lớn.
- Các cảnh nhỏ vẫn phải ở nguyên bối cảnh đính kèm, cùng một nhân vật và cùng trang phục đã khóa trong cấu hình; cắt trên hành động hoặc giữ hướng mắt để tạo cảm giác là một thước phim liên tục.
- Để giảm trôi avatar, giữ mặt ở cỡ medium/medium-close trong phần lớn thời lượng; tránh mở đầu toàn thân quá xa, đi vào khung hình dài, quay đầu nhanh hoặc che mặt. Nhân vật phải hiện rõ ngay từ khung đầu.
- Ưu tiên cảm xúc cận: khoảng 70–80% thời lượng là medium-close, close-up hoặc detail có gương mặt; toàn cảnh chỉ 1–2 giây khi thật sự cần xác lập bối cảnh. Không dùng wide shot kéo dài.
- Mắt là điểm neo chính của cảnh. Prompt phải nêu rõ điểm nhìn và chuyển biến nét mặt ở từng nhịp; máy quay tiến gần chậm, không áp sát quá mức làm biến dạng khuôn mặt.

## Quy tắc thước phim hoàn chỉnh đến khung hình cuối

- Viết 10 giây như một mini-story có động lực liên tục: `0–2,5s thiết lập hành động` → `2,5–6,5s phát triển và tương tác` → `6,5–9,2s cao trào/hoàn tất` → `9,2–10s living finish`.
- Không cho nhân vật hoàn thành hành động ở giây 8 rồi đứng chờ hết video. Hành động chính phải còn tiến triển đến ít nhất giây 9,2.
- Chỉ giảm tốc tự nhiên trong 0,5–0,8 giây cuối. Không dùng `hold final pose for 1.2–1.5 seconds` theo nghĩa bất động; thay bằng `living hero finish` với nhịp thở, chớp mắt, chuyển ánh nhìn nhỏ, quán tính tóc/vải và camera drift 1–2% tới khung hình cuối.
- Mỗi cảnh phải nối bằng động tác đang diễn ra: chân đang đặt xuống, mắt đang chuyển hướng, tay đang siết/đỡ hoặc cơ thể đang xoay. Cảnh sau tiếp tục đúng động lượng, hướng di chuyển và trạng thái cơ thể của cảnh trước.
- Với hành động liên tục như bế, cầm, lái hoặc ôm: khóa trạng thái này ở đầu, giữa và cuối mỗi cảnh; máy quay được đổi vị trí nhưng hành động và quan hệ cơ thể không được reset.
- Cổng kiểm tra bắt buộc: xem ba mốc 0–2s, 4–6s, 8–10s và phát trọn video. Đánh lỗi nếu đoạn 8–10s đứng im, lặp khung, đổi tư thế vô cớ hoặc ngắt câu chuyện trước thời điểm kết.

## Cấu trúc mặc định

## TVC nhiều clip phải là một câu chuyện hành động

Khi người dùng yêu cầu 3 clip/30 giây, không viết ba prompt chỉ khác góc máy. Trước khi tạo phải xác định một chuỗi hành động có nguyên nhân và kết quả:

1. `Clip 1 — Thiết lập và mục tiêu`: cho thấy rõ toàn cảnh, nhân vật bước vào/tiếp cận đúng vị trí và chú ý tới một đối tượng cụ thể trong bối cảnh.
2. `Clip 2 — Hành động chính`: bắt đầu đúng từ trạng thái kết thúc clip 1; nhân vật thực hiện một hành động rõ ràng với đối tượng đó, có điểm bắt đầu, thao tác và kết quả nhìn thấy.
3. `Clip 3 — Kết quả và hero`: bắt đầu từ kết quả clip 2; nhân vật hoàn tất hành động, phản ứng bằng ánh mắt/tư thế, rồi kết thúc ở hero frame.

Mỗi prompt phải ghi rõ `start state`, `ordered actions`, `end state`, hướng di chuyển, tay nào tương tác với vật nào và vị trí của nhân vật trong khung. Khung cuối clip trước phải tương thích với khung đầu clip sau. Không dùng mô tả mơ hồ như `interacts naturally` hoặc `performs a subtle action` nếu không chỉ rõ hành động.

## Độ nét và cảm giác 720p

- Luôn chọn độ phân giải cao nhất trong UI; hiện tại Omni là 720p.
- Trong prompt thêm: `crisp 720p detail, sharp facial features, clean suit fabric texture, high micro-contrast, controlled highlights, low noise, no haze, no soft-focus filter, no motion blur on the face.`
- Không lạm dụng `shallow depth of field`; chỉ làm mờ hậu cảnh nhẹ và luôn giữ mặt, mắt, trang phục cùng vật đang tương tác trong vùng nét.
- Dùng chuyển động máy quay chậm, tốc độ màn trập tự nhiên và ánh sáng đủ mạnh; tránh dolly quá nhanh, orbit rộng hoặc nhân vật quay đầu nhanh vì gây mềm hình.
- 720p là độ phân giải khung, không bảo đảm chi tiết cảm nhận nếu nguồn nhỏ, chủ thể quá xa hoặc có nhiều chuyển động; cổng chất lượng phải đánh giá độ nét thực tế, không chỉ nhãn cấu hình.

## Quy trình khóa bối cảnh bằng Thành phần

1. Dùng Video → Thành phần và gắn Nhân vật trước, Bối cảnh sau.
2. Tuyên bố bối cảnh là không gian bắt buộc, phải nhận ra rõ trong toàn bộ video.
3. Liệt kê các mốc vật thể đặc trưng nhìn thấy trong bối cảnh để khóa kiến trúc, đồ vật, vị trí camera và phối cảnh.
4. Dùng một cú máy liên tục; không cắt cảnh, chuyển phòng hoặc thay trục máy quay.
5. Chỉ tạo một hành động tinh tế để ưu tiên thần thái và độ ổn định.

Mẫu chuẩn đã tạo thành công nằm trong `SKILL.md`, mục `Mẫu prompt Thành phần đã tạo thành công`.

Ưu tiên 2 cảnh để giữ nhận diện ổn định:

1. `0–4 giây` — Hero reveal: khung trung/cận, nhân vật hòa vào bối cảnh thật, ánh mắt và thần thái xuất hiện rõ.
2. `4–10 giây` — Signature action: một hành động tinh tế với đạo cụ/sản phẩm, máy quay tiến nhẹ hoặc chuyển góc mềm, kết thúc bằng hero frame.

Chỉ dùng 3 cảnh khi brief cần tiến triển rõ:

1. `0–3 giây` — Establishing/reveal.
2. `3–7 giây` — Interaction/emotion.
3. `7–10 giây` — Beauty close-up hoặc hero ending.

Không dùng quá 3 cảnh trong một clip 10 giây.

## Quy tắc âm thanh tuyệt đối

- Không viết lời thoại và không tạo kịch bản thoại.
- Không dùng voice-over, spoken words, dialogue hoặc giọng nhân vật.
- Mặc định để nhân vật khép môi tự nhiên; truyền tải nội dung bằng mắt, nét mặt, đầu, vai, tay, dáng đứng và chuyển động máy quay.
- Chỉ thêm nhạc khi người dùng yêu cầu hoặc đã cung cấp nhạc.
- Khi có nhạc, cho phép nhân vật nhép môi rất nhẹ theo nhịp để giữ biểu cảm; không tạo tiếng hát, lời bài hát hoặc phát âm.
- Tránh chuyển động miệng lớn, nhanh hoặc phức tạp vì dễ làm trôi gương mặt.

## Ngôn ngữ hình ảnh

- Sang trọng: bố cục gọn, chất liệu cao cấp, độ tương phản kiểm soát, không phô trương đạo cụ.
- Thần thái: mắt có điểm nhìn, cằm và vai chuyển động nhỏ, tư thế tự tin nhưng tự nhiên.
- Cảm xúc: biểu cảm chuyển nhẹ theo hành động; tránh nụ cười đóng băng hoặc diễn quá mức.
- Lịch lãm: chuyển động chậm, đường nét sạch, khoảng thở, không rung máy.
- Điện ảnh: ánh sáng mềm có hướng, rim light vừa phải, chiều sâu trường ảnh tự nhiên, camera 35–85 mm tùy cảnh.

## Chuyển động phù hợp

- Slow dolly-in, subtle orbit, gentle lateral slide, rack focus nhẹ.
- Nhìn lệch rồi quay mắt về camera.
- Chỉnh kính, chạm sản phẩm, đặt tay lên bàn, bước một nhịp, xoay vai hoặc ngẩng cằm nhẹ.
- Váy, tóc, áo chỉ chuyển động vừa đủ theo môi trường.

Tránh whip pan, zoom gấp, chạy, quay đầu nhanh, biến đổi trang phục hoặc chuyển bối cảnh phi logic.

## Chuẩn chuyển động luxury cinematic

- Mỗi cảnh chỉ có một chuyển động máy chính và một hành động nhân vật chính. Máy quay bắt đầu và kết thúc bằng nhịp easing mềm, không dừng hoặc đổi hướng đột ngột.
- Ưu tiên slow dolly-in 3–5%, lateral slider rất nhẹ hoặc locked camera có parallax tự nhiên; tránh orbit rộng và zoom số.
- Cắt trên hành động: chuyển cảnh đúng lúc tay chạm bàn phím, ánh mắt đổi hướng hoặc nhân vật vừa hoàn tất một cử chỉ để cảm giác liền mạch.
- Chuyển động cơ thể theo thứ tự tự nhiên: mắt → đầu rất nhẹ → vai/tay; không cho nhiều bộ phận chuyển động đồng thời.
- Thần thái sang trọng dùng micro-expression: ánh mắt chắc, chớp mắt chậm tự nhiên, lông mày thay đổi nhỏ, nhịp thở nhẹ, cằm nâng 2–5 độ, vai mở và cổ dài.
- Không cười lớn hoặc tạo dáng khoa trương. Hero ending là một `living hero finish`: ánh mắt ổn định nhưng cơ thể vẫn thở, chớp mắt tự nhiên, tóc/vải còn quán tính và camera tiếp tục drift nhẹ; không đứng hình sớm.
- Ánh sáng ưu tiên soft key có hướng, catchlight rõ trong mắt, rim light mỏng trên vai/tóc và highlights được kiểm soát; thể hiện rõ chất liệu vest, tóc, da và vật liệu bối cảnh.
- Chống cảm giác đơ bằng tín hiệu sống có kiểm soát: chuyển trọng lượng thật theo bước chân, nhịp thở nhẹ, chớp mắt tự nhiên, tóc/vải có quán tính, bàn tay tự điều chỉnh điểm chạm và hậu cảnh có parallax.
- Không dùng cụm `walks slowly` đơn độc. Phải mô tả nhịp bước thời gian thực, điểm đặt chân, chuyển trọng lượng và cách máy quay bắt kịp chuyển động.
- Với hai nhân vật, tạo phản ứng qua lại theo chuỗi: người A nhìn hoặc chạm → người B nhận biết bằng mắt → đầu xoay nhẹ → nét mặt đổi; tránh cả hai cùng đổi biểu cảm một lúc.

## Công thức prompt

Viết bằng tiếng Anh ngắn, rõ và ưu tiên động từ:

1. Khóa tài sản bằng giao diện: gắn đúng avatar/nhân vật và cảnh thật, nhưng trong văn bản chỉ gọi trung tính là `the attached character` và `the attached real scene`.
2. Khóa tính liên tục an toàn: dùng `consistent appearance, hairstyle, wardrobe and accessories throughout the clip`; không dùng tên riêng, `exact identity`, `exact face`, `clone`, `deepfake`, `celebrity`, `public figure` hoặc yêu cầu bắt chước một người thật.
3. Mô tả 2–3 cảnh có mốc thời gian.
4. Mô tả ánh sáng, ống kính và chuyển động máy quay.
5. Khóa tính liên tục và lỗi cần tránh.
6. Luôn kết thúc bằng: `No dialogue, no speech, no voice-over, no spoken words. Mouth stays naturally closed; if music is present, only minimal subtle lip movement with no vocal sound.`

Mẫu 2 cảnh:

`Create a premium vertical cinematic TVC using the attached character and the attached real scene. Keep her appearance, hairstyle, wardrobe and accessories visually consistent throughout the clip. Shot 1, 0–4s: elegant medium hero reveal, the woman holds calm eye contact as the camera slowly dollies in. Shot 2, 4–10s: a refined interaction with the visible product or prop, subtle head turn and confident emotional expression, ending on a polished beauty close-up. Match the real scene perspective, lighting, contact shadows and reflections. Luxury editorial lighting, natural skin texture, stable anatomy and temporal consistency. No extra people, no text, no logo, no outfit change, no warped hands. No dialogue, no speech, no voice-over, no spoken words. Mouth stays naturally closed.`

Thay `character/avatar`, hành động, sản phẩm và camera theo brief thật; không dùng một prompt chung cho mọi bối cảnh.

## Cổng an toàn chính sách trước khi tạo

- Tên riêng chỉ dùng để chọn component trong UI, tuyệt đối không đưa vào văn bản prompt.
- Không mô tả đây là người nổi tiếng hoặc yêu cầu mô phỏng, đóng giả, hoán đổi mặt hay sao chép danh tính.
- Chỉ mô tả nội dung quảng cáo vô hại: tư thế, ánh mắt, cử chỉ, đạo cụ, bối cảnh, ánh sáng và máy quay.
- Nếu bị chặn nhầm, viết lại từ đầu bằng ngôn ngữ trung tính; không gửi lại nguyên văn prompt đã bị chặn.

## Kiểm tra sau render

Xem toàn bộ clip ở tốc độ thường và dừng tại khoảng 0.5s, điểm cắt cảnh, 5s, 8s và khung cuối. So sánh mặt, tóc, miệng, trang phục, tay, đạo cụ, bóng đổ và bối cảnh với tài sản đầu vào. Nghe lại để chắc chắn không có thoại hoặc giọng nói.
