---
name: "dao-dien-trieu-view"
description: "Đạo diễn phim ngắn AI - biến chủ đề hoặc kịch bản có sẵn cùng thời lượng thành gói sản xuất video hoàn chỉnh (ý tưởng, kịch bản theo timecode, nhịp giữ chân, shot list, hồ sơ nhân vật khóa nhận dạng và giọng, ảnh từng cảnh) rồi xuất flow-manifest để dựng tự động trên Google Flow. Dùng khi người dùng gọi Đạo diễn triệu view, muốn làm phim ngắn, short drama, Reels, TikTok, Shorts từ một chủ đề, viết kịch bản phân cảnh, storyboard, hoặc nhắc kèm một skill làm phim khác."
---

# Đạo diễn triệu view

Biến brief ngắn thành một tác phẩm có chủ đích sáng tạo và đủ chi tiết để sản xuất. "Triệu view" là tiêu chuẩn tối ưu sức hút, cảm xúc và khả năng chia sẻ, không phải lời bảo đảm lượt xem.

Đây là khâu 1 của dây chuyền 3 skill:
1. **dao-dien-trieu-view** (skill này): ý tưởng → kịch bản → nhân vật khóa nhận dạng → ảnh cảnh → `flow-manifest.json`
2. **flow-dung-phim-tu-dong**: manifest → clip Google Flow → ghép → MP4
3. **phat-hanh-video-da-nen-tang**: MP4 đã duyệt → caption từng nền tảng → đăng

## 1. Quy tắc cốt lõi

- **Chủ đề + thời lượng là đủ để bắt đầu.** Tự đặt giả định hợp lý và ghi rõ ở đầu kết quả. Chỉ hỏi khi thiếu một lựa chọn làm thay đổi căn bản tác phẩm.
- **Chỉ báo những gì thật sự đã làm.** Không nói "đã tạo ảnh", "đã khóa nhân vật" hay "đã xuất manifest" khi file chưa tồn tại. Ảnh chưa tạo được thì nói rõ là mới có prompt.
- **Lỗi là dừng.** Công cụ tạo ảnh báo lỗi, hết hạn mức hoặc từ chối prompt thì dừng bước đó, báo nguyên văn lỗi và cách xử lý. Không tự đổi sang công cụ khác hay nghĩ ra cách vòng mà người dùng chưa biết.
- **Không ghi đè dự án cũ.** Nếu `outputs/<slug>/` đã có dữ liệu, tạo slug mới (thêm `-v2`, `-v3`). Chỉ làm lại trên chính dự án cũ khi người dùng yêu cầu rõ, và phải xác nhận hai lần: lần 1 hỏi có muốn làm lại dự án đó không; lần 2 nói rõ kịch bản, ảnh, manifest cũ sẽ bị thay rồi mới làm.
- Tôn trọng sự thật, quyền riêng tư, bản quyền và an toàn. Không vẽ nhân vật có bản quyền hay người thật có danh tính khi chưa được phép. Không hứa "bảo đảm viral".

## 2. Skill nguồn được nhắc kèm

Khi người dùng nhắc tên skill làm phim khác (ví dụ "đạo diễn triệu view + skill mẹ chồng nàng dâu", hoặc gõ `/ten-skill`), coi đó là **skill nguồn được chỉ định**:

1. Tải skill đó (Skill tool) và đọc toàn bộ hướng dẫn, cùng các tài liệu nó yêu cầu cho đúng việc đang làm.
2. Rút ra 2–4 "vũ khí đặc trưng": kiểu kể chuyện, ngôn ngữ hình ảnh, nhịp dựng, giới hạn bắt buộc. Thể hiện chúng trong sản phẩm, không chỉ nhắc tên.
3. Nhiều skill nguồn: phân vai (nội dung / hình ảnh / chuyển động / âm thanh / dựng) và chọn một phong cách chủ đạo để phim không chắp vá.
4. Trước sản phẩm ghi một dòng: `Đã khai thác: <skill> — vai trò …`.
5. Skill không tồn tại hoặc không đọc được: báo đúng tên bị thiếu. Không âm thầm thay bằng skill khác.

Không có skill nguồn: tự làm bằng hướng dẫn trong skill này. Nếu người dùng gửi kịch bản, đọc toàn bộ trước; giữ nguyên dữ kiện cốt lõi họ muốn bảo toàn.

## 3. Quy trình

Dùng task list cho cả quy trình. Mỗi khâu xong thì đánh dấu.

### Bước 1 — Giải mã brief

Xác định: chủ đề, thời lượng, nền tảng, tỷ lệ khung, khán giả, cảm xúc đích, giọng điệu, mức hiện thực, đầu ra mong muốn. Mặc định với video ngắn: dọc 9:16, xem trên điện thoại, nhịp nhanh nhưng dễ hiểu, tiếng Việt, bối cảnh Việt Nam nếu chủ đề cho phép.

Chọn **chế độ chạy**:
- **Duyệt từng chặng** (mặc định): dừng ở CP1 và CP2 bên dưới để người dùng duyệt.
- **Chạy liền**: khi người dùng nói "làm hết", "chạy liền", "tự động". Vẫn báo kết quả ở mỗi checkpoint nhưng không chờ.

### Bước 2 — Sao Bắc Đẩu sáng tạo

Chốt 6 yếu tố trong vài dòng trước khi viết cảnh:
1. **Hình ảnh mở màn**: hành động, vật thể hoặc mâu thuẫn hiểu được ngay cả khi tắt tiếng.
2. **Lời hứa**: điều cụ thể người xem sẽ biết, cảm hoặc chứng kiến nếu ở lại.
3. **Câu hỏi trung tâm**: câu hỏi chưa có lời đáp, kéo người xem đến cuối.
4. **Đường cong cảm xúc**: bắt đầu → áp lực tăng → đảo chiều → dư vị.
5. **Chi tiết biểu tượng**: một vật, âm thanh hoặc cử chỉ đổi nghĩa trong truyện.
6. **Payoff**: câu trả lời, lựa chọn hoặc hình ảnh cuối trả đủ lời hứa.

Chỉ chọn **một** ý tưởng đủ mạnh. Loại ý tưởng nếu: đổi tên nhân vật mà truyện vẫn y nguyên; xung đột chỉ nằm trong lời thoại, không quay được; phản diện xấu tuyệt đối không có động cơ; cú lật dựa vào thông tin chưa gieo; mọi cảnh cùng nhịp, cùng cỡ cảnh; kết bằng bài giảng.

Cơ chế giữ chân (chọn cái hợp, không nhồi tất cả): cold open, open loop, escalation (mỗi beat mất thêm một lựa chọn hoặc đổi cán cân quyền lực), recontextualization, pattern interrupt có lý do, micro-payoff, moral friction (hai phía đều có lý để khán giả muốn bình luận). Video ngắn: khung hoặc câu đầu tiên phải chứa mâu thuẫn cụ thể, không chào hỏi.

Mỗi nhân vật chính cần: điều muốn ngay trong cảnh, điều sợ mất, chiến thuật, một hành động lộ bản chất, giọng nói riêng. Thoại có subtext; ánh mắt, đạo cụ, khoảng lặng gánh phần nghĩa còn lại.

### Bước 3 — Bible nhân vật, bối cảnh, đạo cụ (khóa nhận dạng)

Đây là phần học từ DramaClaw: **nhân vật được giữ nhất quán bằng ảnh nhận dạng, không bằng tên.**

Gán mã cố định và ghi vào bible:
- **Nhân vật `NV01`, `NV02`…**: tên; tuổi ước lượng; khuôn mặt (dáng mặt, mắt, tóc, nốt ruồi/đặc điểm); vóc dáng; trang phục và phụ kiện cố định; tính khí; mục tiêu; **giọng nói** (giới tính, tuổi giọng, vùng miền, tốc độ, sắc thái). Ghi rõ đặc điểm nào **không được đổi** và đặc điểm nào được đổi theo diễn biến (ví dụ: tóc rối sau cảnh cãi nhau).
- **Bối cảnh `BC01`…**: không gian, thời điểm, hướng sáng, bảng màu, vật thể cố định.
- **Đạo cụ `DC01`…**: chỉ những vật có vai trò trong truyện (vật chứng, chi tiết biểu tượng).

Nhân vật chỉ xuất hiện thoáng qua, không thoại, không cần mã riêng.

### Bước 4 — Nhịp và kịch bản theo timecode

Chia thời lượng thành cảnh có timecode. Mỗi cảnh phải làm ít nhất một việc: đưa thông tin mới, tăng xung đột, đổi quyền lực, gây bất ngờ, tạo cảm xúc hoặc trả lời câu hỏi đã gieo. Cắt cảnh chỉ lặp ý cũ. Thoại tiếng Việt kịch tính: khoảng 120–150 từ/phút, chừa chỗ cho biểu cảm, khoảng lặng và âm thanh.

Số cảnh theo thời lượng: dưới 30 giây ít bối cảnh, một ý, payoff nhanh; 30–90 giây nhiều beat, một lần đảo chiều rõ; trên 90 giây thêm nhịp thở, phát triển nhân vật. Mỗi cảnh nên dài vừa một clip Flow (thường 4–8 giây). Cảnh dài hơn thì tách thành shot `C03-S02`, hoặc thành nhiều cảnh.

Bảng kịch bản master:

| Cảnh | Timecode | Nhân vật (mã) | Bối cảnh | Mục tiêu beat | Hình ảnh & hành động | Thoại (người nói: câu) | Máy quay & ánh sáng | Âm thanh | Chuyển cảnh | Móc giữ chân |
|---|---|---|---|---|---|---|---|---|---|---|

Quy tắc:
- Tổng thời lượng các cảnh bằng thời lượng mục tiêu, sai số tối đa 1 giây.
- Ghi lời thoại thật, gắn với mã người nói (`NV01: …`, hoặc `VO: …` cho lời dẫn). Không viết kiểu "nhân vật nói về việc…".
- Chữ trên màn hình chỉ khi tăng hiểu biết hoặc nhịp.
- Chuyển cảnh nói rõ điểm nối: match cut theo vật/chuyển động/màu, sound bridge, whip pan, hard cut, J-cut/L-cut, fade có dụng ý.

Sau bảng, kèm **retention map** theo timecode (hook, open loop, các lần tăng áp lực, pattern interrupt, micro-payoff, reveal, payoff, CTA hoặc loop ending). CTA không được phá cảm xúc đoạn kết.

**CP1 — duyệt kịch bản.** Ở chế độ duyệt từng chặng: gửi concept + bible + kịch bản, hỏi người dùng duyệt hoặc sửa trước khi tạo ảnh (vì tạo ảnh tốn hạn mức).

### Bước 5 — Ảnh nhận dạng trước, ảnh cảnh sau

Thứ tự bắt buộc:
1. **Ảnh nhận dạng nhân vật** `identity/NV01-<ten>.png`: chính diện hoặc 3/4, toàn thân hoặc nửa người, nền trơn, đúng trang phục cố định, ánh sáng đều. Có thể làm character sheet nhiều góc nếu công cụ hỗ trợ.
2. **Ảnh bối cảnh** `locations/BC01.png` và **đạo cụ** `props/DC01.png` khi cần.
3. Tự soát từng ảnh nhận dạng với bible (mặt, tóc, trang phục, màu). Sai thì tạo lại trước khi đi tiếp. Ảnh nhận dạng sai sẽ kéo sai toàn bộ phim.

**CP2 — duyệt nhận dạng.** Ở chế độ duyệt từng chặng: gửi các ảnh nhận dạng, chờ người dùng chốt. Sau khi chốt, ảnh nhận dạng **bị khóa**: không tạo lại trừ khi người dùng yêu cầu. Nếu người dùng đổi ảnh nhận dạng của một nhân vật, liệt kê mọi cảnh có nhân vật đó vì chúng phải làm lại.

4. **Ảnh khung đầu từng cảnh** `images/C001-start.png` (và `C001-end.png` khi cảnh biến đổi lớn hoặc cần match cut sang cảnh sau). Khi công cụ nhận ảnh tham chiếu, **luôn đưa ảnh nhận dạng của mọi nhân vật trong cảnh + ảnh bối cảnh** vào, thay vì tạo độc lập.

Prompt keyframe theo thứ tự: định dạng và phong cách → nhân vật kèm đặc điểm khóa (lặp lại mô tả hữu hình, không dựa vào tên) → hành động và biểu cảm tại beat → bối cảnh, đạo cụ → bố cục, cỡ cảnh, góc → ánh sáng, màu → tỷ lệ khung, vùng trống cho chữ. Negative prompt chỉ ghi lỗi thật cần tránh: đổi mặt/trang phục, thừa ngón, sai đạo cụ, chữ hoặc logo lạ, bối cảnh sai thời đại.

Công cụ tạo ảnh: dùng skill hoặc công cụ tạo ảnh đang có trong phiên (ví dụ skill tạo ảnh qua API mà người dùng đã cài), hoặc trình tạo ảnh ngay trong Google Flow nếu tài khoản có. Đọc hướng dẫn của công cụ đó trước khi dùng. Không có công cụ nào thì dừng ở prompt, nói rõ như vậy, và vẫn xuất manifest với `status: "draft"` cho các cảnh thiếu ảnh.

Mỗi ảnh xong: đối chiếu với mã cảnh và bible. Sai chi tiết cốt truyện hoặc sai nhận dạng thì tạo lại (tối đa 2 lần mỗi ảnh, trừ khi người dùng cho thêm).

Mỗi keyframe kèm một dòng **motion direction**: chuyển động nhân vật, chuyển động máy, thay đổi ánh sáng/môi trường, điểm bắt đầu–kết thúc, điều phải giữ cố định. Tránh camera bay lắc vô cớ, nhiều chủ thể chuyển động cùng lúc.

### Bước 6 — Hậu kỳ và tiêu đề

Ghi: nhịp cắt từng đoạn; hướng nhạc (không sao chép bài có bản quyền); SFX/foley cụ thể; cách đặt phụ đề; grade màu; khung làm thumbnail; 3 tiêu đề/caption xếp hạng và đề xuất 1.

### Bước 7 — Tự duyệt im lặng

Trước khi giao, tự hỏi và sửa nếu yếu (không trình điểm số trừ khi được hỏi):
- Hook hiểu được khi tắt tiếng trong 1–2 giây đầu?
- Cứ vài giây có thông tin, cảm xúc hoặc hình ảnh mới?
- Mâu thuẫn leo thang, cán cân quyền lực đổi?
- Cú lật đã được gieo, hợp logic?
- Chuyển cảnh có động cơ hình ảnh hoặc âm thanh?
- Thời lượng cảnh cộng lại khớp tổng?
- Thoại giống người thật, mỗi nhân vật một giọng, diễn được?
- **Nhận dạng**: mọi ảnh cảnh khớp ảnh nhận dạng của từng nhân vật (mặt, tóc, trang phục)? Bối cảnh và đạo cụ nhất quán?
- Cái kết trả được lời hứa của hook?

## 4. Bàn giao

Cấu trúc thư mục dự án (trong thư mục làm việc; nếu máy người dùng đang kết nối và họ chỉ định thư mục, ghi thêm vào đó):

```text
outputs/<project-slug>/
|-- goi-san-xuat.md              concept, bible, kịch bản, retention map, hậu kỳ, tiêu đề
`-- flow-handoff/
    |-- flow-manifest.json
    |-- identity/NV01-<ten>.png  ảnh nhận dạng nhân vật
    |-- locations/BC01.png
    |-- props/DC01.png
    `-- images/C001-start.png …
```

`project-slug`: chữ thường không dấu, số, gạch ngang (ví dụ `me-chong-giu-vang-cuoi`).

### flow-manifest.json (schema 2)

```json
{
  "schema_version": 2,
  "project": {"slug": "me-chong-giu-vang-cuoi", "title": "Mẹ chồng giữ vàng cưới", "flow_project_name": "DDTV-me-chong-giu-vang-cuoi"},
  "target": {"aspect_ratio": "9:16", "duration_seconds": 90, "language": "vi", "platform": "Facebook Reels"},
  "characters": [
    {"id": "NV01", "name": "Mẹ chồng", "identity_ref": "identity/NV01-me-chong.png",
     "locked_traits": "khoảng 55 tuổi, tóc búi thấp hoa râm, áo bà ba tím than, vòng ngọc xanh tay trái",
     "voice": "nữ trung niên, giọng Bắc, chậm, lạnh"}
  ],
  "locations": [{"id": "BC01", "name": "Phòng khách nhà chồng", "ref": "locations/BC01.png", "locked_traits": "tủ thờ gỗ, ánh đèn vàng ấm"}],
  "props": [{"id": "DC01", "name": "Hộp vàng cưới đỏ", "ref": "props/DC01.png"}],
  "continuity": {"style": "cinematic family drama, realistic Vietnamese setting", "notes": "Không đổi khuôn mặt, trang phục cưới và hộp vàng."},
  "scenes": [
    {
      "id": "C001", "order": 1, "title": "Bàn tay lấy hộp vàng",
      "desired_duration_seconds": 6, "generation_mode": "frames",
      "cast": ["NV01"], "location": "BC01", "props": ["DC01"],
      "start_image": "images/C001-start.png", "end_image": null,
      "ingredients": ["identity/NV01-me-chong.png", "props/DC01.png"],
      "motion_prompt": "Slow push-in as the mother-in-law quietly pulls the red jewelry box toward herself; restrained tension; keep face, hair bun and purple ao ba ba unchanged.",
      "dialogue": [{"speaker": "NV01", "line": "Số vàng này… mẹ giữ hộ."}],
      "audio_direction": "Room tone, faint wedding music, jewelry box clasp click.",
      "transition_out": "Sound bridge of the clasp into the next scene.",
      "trim_in": 0, "trim_out": 0, "status": "approved"
    }
  ],
  "assembly": {"scene_order": ["C001"], "caption_mode": "none", "audio_strategy": "flow_native", "final_filename": "me-chong-giu-vang-cuoi-final.mp4"}
}
```

Quy tắc manifest:
- Mọi đường dẫn là tương đối từ thư mục `flow-handoff/`, không dùng `..`.
- `cast` liệt kê mã mọi nhân vật lộ mặt trong cảnh; `ingredients` nên chứa `identity_ref` của họ. Nếu chế độ Flow của cảnh không nhận ingredients, ảnh khung đầu phải được tạo từ ảnh nhận dạng.
- `dialogue[].speaker` là mã nhân vật hoặc `VO`.
- `status: "approved"` chỉ khi cảnh đã có đủ ảnh và người dùng đã duyệt (hoặc đang ở chế độ chạy liền). Cảnh thiếu ảnh để `draft`; khâu Flow sẽ không tốn credit cho cảnh `draft`.
- `motion_prompt` viết tiếng Anh cho model video, tập trung vào chuyển động, máy, ánh sáng, âm thanh và những gì phải giữ nguyên; không tả lại dài những gì ảnh đã khóa.
- Nếu skill flow-dung-phim-tu-dong có `scripts/validate_manifest.py`, chạy nó để kiểm tra trước khi bàn giao.

### Gửi cho người dùng

- Gửi file `goi-san-xuat.md` và ảnh nhận dạng, ảnh cảnh chính (gửi file, không chỉ đưa đường dẫn).
- Trong chat chỉ tóm tắt ngắn: concept một câu, số cảnh, tổng thời lượng, số ảnh đã tạo / còn thiếu, giả định đã đặt.
- Nếu người dùng muốn dựng tiếp, chuyển sang skill **flow-dung-phim-tu-dong** với manifest vừa tạo. Ở chế độ chạy liền mà người dùng đã yêu cầu dựng video, gọi luôn skill đó.

## 5. Sửa sau khi đã giao

Thứ tự cố định khi người dùng sửa một cảnh (học từ DramaClaw):
1. Sửa nội dung cảnh trong `goi-san-xuat.md` và manifest trước.
2. Tạo lại đúng ảnh của cảnh bị ảnh hưởng.
3. Báo khâu Flow rằng cảnh đó cần dựng lại (đặt lại `status` của cảnh và ghi chú lý do).

Không sửa ảnh mà quên cập nhật manifest, và không làm lại toàn bộ phim khi chỉ một cảnh đổi.

## Cách gọi mẫu

- `Đạo diễn triệu view. Chủ đề: mẹ chồng giữ vàng cưới của nàng dâu. Thời lượng: 1 phút 30 giây. Làm trọn bộ kịch bản và ảnh từng cảnh.`
- `Dùng đạo diễn triệu view với skill <tên skill nguồn>, kịch bản đính kèm, 60 giây, chạy liền rồi dựng luôn trên Flow.`