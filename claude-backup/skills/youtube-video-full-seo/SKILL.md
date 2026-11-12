---
name: "youtube-video-full-seo"
description: "SEO đầy đủ cho 1 video YouTube mới đăng trên kênh Phong Menly AI Go Global (chưa public) — timeline, thẻ (cards), màn hình kết thúc, từ khóa, tiêu đề, mô tả, hashtag. Dùng khi chủ kênh giao \"SEO video mới\" hoặc \"video chưa được SEO\"."
---

# SEO đầy đủ 1 video YouTube (Chi tiết video trong YouTube Studio)

## Khi nào dùng

Khi được giao SEO toàn diện cho 1 video cụ thể vừa upload (thường chưa public,
"Không công khai"), theo yêu cầu đầy đủ: "Màn hình kết thúc, Thẻ tag, Từ khóa,
Tiêu đề, Mô tả, Timeline, Hashtag" — không chỉ 1 phần riêng lẻ.

## Checklist theo thứ tự làm

1. **Timeline (chương video)**: Dùng **Hỏi Studio** (AI assistant có sẵn trong
   YouTube Studio, nút "Hỏi Studio" trên thanh top nav) để nhờ AI phân tích nội
   dung/transcript thật của video và tạo danh sách chương có mốc thời gian —
   không tự bịa timeline.
   - **Lưu ý paste bị chặn**: Ctrl+V vào textarea của Studio bị trình duyệt
     chặn (không đổi số ký tự). Lấy nguyên văn kết quả AI bằng cách đọc
     `textContent` của phần tử chat qua `javascript_tool` (vì `read_page`/`find`
     cắt ngắn text dài ~100 ký tự bất kể `max_chars`), rồi gõ lại bằng công cụ
     gõ phím thật (`type` action), không gán `.value` trực tiếp.
   - **Thứ tự trong Mô tả — timeline KHÔNG đặt ở đầu**: dán/gõ timeline gần
     cuối phần Mô tả (ngay trước hashtag), không đặt ở đầu. Phần đầu Mô tả
     dành cho nội dung quan trọng nhất (đoạn intro/hook + khối Affiliate/công
     cụ AI/liên hệ chuẩn) — xem thứ tự đầy đủ ở bước 6.
2. **Thẻ (Cards)**: Vào mục "Thẻ" ở sidebar phải → thêm 2 video cùng chủ đề
   liên quan → Lưu.
3. **Màn hình kết thúc (End Screen)**: Vào mục "Màn hình kết thúc" → chọn mẫu
   "2 video" → định vị đúng ~20 giây cuối video → chọn 2 video liên quan cho 2
   ô. Nếu cần chọn video cụ thể giữa danh sách dài, **dùng ô tìm kiếm gõ đúng
   tên video** thay vì cuộn+bấm tọa độ (cuộn dễ bị lệch giữa các lần chụp màn
   hình, dẫn đến bấm nhầm video khác).
4. **Từ khóa (Thẻ từ khóa)**: Thêm từ khóa tìm kiếm/đề xuất/liên quan vào ô
   "Thẻ (từ khóa)" trong Chi tiết video (giới hạn 500 ký tự, phân tách bằng
   dấu phẩy).
   - **Lỗi thường gặp — chip bị hỏng**: Nếu gõ nguyên một chuỗi dài nhiều từ
     khóa cách nhau bởi dấu phẩy bằng `type` action trong khi con trỏ đang nằm
     trong 1 chip có sẵn (ví dụ chip cuối cùng đang ở chế độ chỉnh sửa), YouTube
     Studio có thể **không tách chip theo dấu phẩy** và nối luôn text mới vào
     cuối chip cũ (vd "ai go global" + text mới dính liền thành 1 chip duy
     nhất, không dấu cách). Luôn kiểm tra lại bằng cách đọc DOM (xem dưới) sau
     khi gõ, đừng chỉ tin ảnh chụp màn hình.
   - **Phím Backspace/Delete/Ctrl+A không luôn hoạt động** trên ô chip này
     (khác với ô Mô tả). Nếu cần sửa 1 chip bị lỗi mà phím tắt không ăn, dùng
     JS: lấy `input#text-input` đúng chip qua deep-query xuyên shadow DOM, set
     giá trị bằng native setter rồi dispatch `input` event, sau đó bấm phím
     Enter thật để chốt chip:
     ```js
     function deepQueryAll(root, selector, results = []) {
       for (const el of root.querySelectorAll('*')) {
         if (el.matches(selector)) results.push(el);
         if (el.shadowRoot) deepQueryAll(el.shadowRoot, selector, results);
       }
       return results;
     }
     const target = deepQueryAll(document, 'input#text-input').find(i => i.value.includes('<phần lỗi>'));
     Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set.call(target, '<giá trị đúng>');
     target.dispatchEvent(new Event('input', {bubbles: true, composed: true}));
     ```
     rồi bấm phím Enter (qua `computer` tool) để chốt thành chip riêng.
   - **Cách an toàn nhất để thêm nhiều từ khóa mới**: gõ **từng cụm một** rồi
     **click ra ngoài ô (blur) để chốt** — không dựa vào phím Enter (không ổn
     định trên ô này, có lúc không chốt chip mà nối luôn vào cụm gõ tiếp theo)
     và không gõ nguyên chuỗi dài nhiều dấu phẩy trong 1 lần `type` (auto-tách
     theo dấu phẩy cũng không ổn định, có lúc gộp hết thành 1 chip).
   - Xác minh kết quả cuối bằng deep-query `ytcp-chip` (xuyên shadow DOM) để
     lấy danh sách chip thật, đối chiếu với danh sách từ khóa định thêm —
     không tin ảnh chụp màn hình vì có thể bị cắt/che bởi tooltip.
   - **Số lượng & loại từ khóa**: đừng dừng ở vài từ khóa ngắn chung chung.
     Kết hợp từ khóa ngắn (chủ đề/thương hiệu) với **từ khóa dài dạng cụm tìm
     kiếm thật** (4-6 từ, mô phỏng câu người dùng gõ tìm, ví dụ "cách kiếm
     1000 đô từ youtube", "kinh nghiệm làm youtube") để tăng tỉ lệ cạnh tranh/
     được đề xuất cho từ khóa ngách. Lấp gần đầy ngân sách 500 ký tự thay vì
     chỉ thêm "cho đủ có".
5. **Tiêu đề**: Đối chiếu format với các tiêu đề video win (lấy top view cao
   nhất của kênh qua trang "Nội dung", sắp xếp giảm dần theo Lượt xem — có thể
   dùng URL `https://studio.youtube.com/channel/<ID kênh>/videos/upload?filter=[]&sort={"columnType":"views","sortOrder":"DESCENDING"}`).
   Nhận diện pattern chung (số liệu cụ thể, cấu trúc "X: Y" hoặc dấu gạch "–",
   từ khóa hot theo chủ đề, Title Case) — chỉ chỉnh nếu tiêu đề hiện tại thực
   sự lệch pattern, không ép nhồi từ khóa không liên quan chủ đề video.
6. **Mô tả**: Áp dụng skill `youtube-description-standardizer` để đảm bảo khối
   mặc định (Affiliate/công cụ AI/Telegram) đúng bản chuẩn mới nhất — nếu mô tả
   đang có bản cũ/khác của khối này thì thay toàn bộ, giữ nguyên phần
   intro/hashtag riêng của video.
   - **Thứ tự chuẩn cả khối Mô tả** (thông tin quan trọng lên trên, timeline
     xuống gần cuối):
     1. Đoạn intro/hook (giới thiệu giá trị video)
     2. Khối chuẩn Affiliate + công cụ AI + liên hệ/Telegram
     3. Timeline/chương (00:00 - ...)
     4. Hashtag (luôn ở cuối cùng)
7. **Hashtag**: Xác nhận hashtag cuối mô tả đã có và phù hợp chủ đề video;
   không tự thêm hashtag mới ngoài phạm vi skill mô tả trừ khi được yêu cầu.
8. **Lưu**: Bấm nút "Lưu" ở đầu trang Chi tiết video, sau đó xác nhận đã lưu
   thành công bằng cách kiểm tra thuộc tính `disabled` của nút (qua deep-query
   `ytcp-button` có text "Lưu") — nút chuyển `disabled: true` nghĩa là đã lưu.
   Card/End Screen lưu riêng theo dialog của chúng, không phụ thuộc nút Lưu
   chính này.

## Ghi chú kỹ thuật chung

- Trang Chi tiết video của YouTube Studio dùng Polymer + shadow DOM sâu, nên
  `document.querySelectorAll` thường không tìm thấy phần tử — luôn dùng hàm
  deep-query xuyên `shadowRoot` như trên khi cần đọc/sửa DOM bằng JS.
- Ảnh chụp màn hình trong môi trường này có thể bị scale xuống so với viewport
  thật (vd 800x745 so với 1252x1167) — ưu tiên click bằng `ref` (từ
  `find`/`read_page`) thay vì tọa độ thô để tránh bấm trượt.