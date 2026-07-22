# Video Editor (thử nghiệm)

Ứng dụng chỉnh sửa video chạy hoàn toàn trong trình duyệt, dùng [ffmpeg.wasm](https://ffmpegwasm.netlify.app/) — không có backend, video không rời khỏi máy người dùng.

## Tính năng

- **Cắt video (trim)** — cắt một đoạn video theo thời gian bắt đầu/kết thúc.
- **Ghép video (merge)** — nối nhiều video lại theo thứ tự, tự động scale về cùng độ phân giải. Nếu tất cả video đầu vào đều có audio thì audio cũng được ghép; nếu có video câm, audio sẽ bị bỏ qua trong kết quả.
- **Chèn text / watermark** — vẽ chữ lên canvas rồi overlay lên video ở 1 trong 5 vị trí (4 góc + giữa).
- **Đổi định dạng / nén (convert)** — chuyển sang MP4/WebM/GIF, tuỳ chọn giảm độ phân giải và mức nén (CRF).

## Chạy thử

```bash
npm install
npm run dev
```

Mở địa chỉ mà Vite in ra (mặc định `http://localhost:5173`).

`npm install` sẽ tự copy file core của ffmpeg.wasm (`ffmpeg-core.js` + `ffmpeg-core.wasm`, ~30MB) từ `node_modules/@ffmpeg/core` vào `public/ffmpeg-core/` (qua script `scripts/copy-ffmpeg-core.js`) để ứng dụng tự host core, không phụ thuộc CDN bên ngoài.

## Build production

```bash
npm run build
npm run preview
```

## Giới hạn

- Xử lý bằng WebAssembly một luồng nên sẽ chậm hơn ffmpeg native, đặc biệt với video dài/độ phân giải cao.
- Tính năng ghép video giả định các clip có cùng loại audio (có hoặc không có); không hỗ trợ hoà trộn giữa audio nhiều kênh khác nhau.
