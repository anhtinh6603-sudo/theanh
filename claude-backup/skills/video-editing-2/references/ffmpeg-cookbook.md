# FFmpeg Cookbook

Tham khảo lệnh theo từng nhóm tác vụ. `-y` = tự động ghi đè output nếu trùng tên
(bỏ đi nếu muốn hỏi trước khi ghi đè).

---

## 1. Cắt / Ghép video

### Cắt 1 đoạn (trim) — nhanh, không encode lại (giữ nguyên chất lượng)
```bash
ffmpeg -ss 00:00:10 -to 00:00:25 -i input.mp4 -c copy output.mp4
```
- `-ss` thời điểm bắt đầu, `-to` thời điểm kết thúc (định dạng HH:MM:SS hoặc giây)
- `-c copy`: cắt nhanh nhưng điểm cắt có thể lệch vài frame vì cắt theo keyframe gần nhất

### Cắt chính xác từng frame (chậm hơn, encode lại)
```bash
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:25 -c:v libx264 -c:a aac output.mp4
```
Đặt `-ss` SAU `-i` để chính xác đến frame (chậm hơn vì phải decode từ đầu).

### Ghép nhiều video cùng codec/định dạng (nhanh)
```bash
# Tạo file danh sách
cat > filelist.txt << EOF
file 'clip1.mp4'
file 'clip2.mp4'
file 'clip3.mp4'
EOF

ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

### Ghép video khác codec/độ phân giải (encode lại, an toàn hơn)
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex \
  "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```
Mở rộng cho N clip: thêm `-i clipN.mp4` và nối thêm `[N:v][N:a]` vào filter,
sửa `n=2` thành số clip tương ứng.

---

## 2. Đổi định dạng / Nén / Đổi độ phân giải

### Convert định dạng đơn giản
```bash
ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4
```

### Nén video giảm dung lượng (giữ chất lượng hợp lý)
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```
- `-crf`: 0 (lossless) đến 51 (tệ nhất). 18-23 là vùng "nhìn ổn", 23-28 nén mạnh hơn
- `-preset`: ultrafast → veryslow. Chậm hơn = nén hiệu quả hơn cùng chất lượng

### Đổi độ phân giải
```bash
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4
```
Giữ tỷ lệ khung hình (chiều rộng tự tính theo chiều cao 720, chia hết cho 2):
```bash
ffmpeg -i input.mp4 -vf "scale=-2:720" -c:a copy output.mp4
```

### Nén mạnh cho web/chia sẻ (dung lượng nhỏ nhất có thể chấp nhận được)
```bash
ffmpeg -i input.mp4 -vf "scale=-2:720" -c:v libx264 -crf 28 -preset slow \
  -c:a aac -b:a 96k output.mp4
```

---

## 3. Phụ đề & Chữ overlay

### Gắn cứng phụ đề từ file .srt vào video (burn-in, không tắt được)
```bash
ffmpeg -i input.mp4 -vf "subtitles=phude.srt" -c:a copy output.mp4
```
Nếu đường dẫn có khoảng trắng/ký tự đặc biệt hoặc trên Windows, escape đường dẫn:
```bash
ffmpeg -i input.mp4 -vf "subtitles=phude.srt:force_style='FontSize=24'" -c:a copy output.mp4
```

### Gắn phụ đề mềm (tắt/bật được, không encode lại video)
```bash
ffmpeg -i input.mp4 -i phude.srt -c copy -c:s mov_text output.mp4
```
(dùng cho .mp4; container khác như .mkv có thể giữ nguyên .srt bằng `-c:s srt`)

### Thêm chữ overlay tùy chỉnh (text cố định, không phải phụ đề theo timeline)
```bash
ffmpeg -i input.mp4 -vf "drawtext=text='Nội dung chữ':fontcolor=white:fontsize=36:\
x=(w-text_w)/2:y=h-th-30:box=1:boxcolor=black@0.5:boxborderw=10" \
  -c:a copy output.mp4
```
- `x`/`y`: vị trí (công thức trên = canh giữa ngang, cách đáy 30px)
- Cần font hỗ trợ tiếng Việt có dấu, thêm `fontfile=/path/to/font.ttf` nếu font
  mặc định không hiển thị được dấu tiếng Việt

---

## 4. Âm thanh

### Tách âm thanh ra file riêng
```bash
ffmpeg -i input.mp4 -vn -c:a copy audio.aac
# hoặc xuất mp3:
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
```

### Xóa âm thanh khỏi video
```bash
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```

### Thay âm thanh khác cho video (âm thanh mới phải cùng/dài hơn video)
```bash
ffmpeg -i input.mp4 -i nhac_moi.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4
```

### Thêm nhạc nền, giữ nguyên âm thanh gốc (trộn 2 track)
```bash
ffmpeg -i input.mp4 -i nhac_nen.mp3 -filter_complex \
  "[0:a]volume=1.0[a0];[1:a]volume=0.3[a1];[a0][a1]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy output.mp4
```
- `volume=0.3` giảm âm lượng nhạc nền còn 30% để không át giọng nói
- `duration=first`: độ dài output theo track đầu (video gốc)

---

## 5. GIF từ video

### Cách chuẩn (chất lượng tốt, dùng palette 2 bước)
```bash
ffmpeg -i input.mp4 -ss 5 -t 3 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -ss 5 -t 3 -i palette.png -filter_complex \
  "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```
- `-ss 5 -t 3`: bắt đầu giây thứ 5, lấy 3 giây
- `fps=15`: giảm khung hình cho file nhẹ hơn (GIF gốc thường 10-15fps là đủ mượt)

---

## 6. Xoay / Lật / Crop / Tốc độ

### Xoay video 90 độ theo chiều kim đồng hồ
```bash
ffmpeg -i input.mp4 -vf "transpose=1" -c:a copy output.mp4
```
(`transpose=0` ngược chiều kim đồng hồ, `transpose=2` ngược chiều + lật)

### Lật ngang / lật dọc
```bash
ffmpeg -i input.mp4 -vf "hflip" -c:a copy output.mp4   # lật ngang
ffmpeg -i input.mp4 -vf "vflip" -c:a copy output.mp4   # lật dọc
```

### Crop (cắt khung hình, không phải cắt thời gian)
```bash
ffmpeg -i input.mp4 -vf "crop=w:h:x:y" -c:a copy output.mp4
# ví dụ crop vùng 720x1280 bắt đầu từ góc (100,0) - dùng cho làm video dọc
ffmpeg -i input.mp4 -vf "crop=720:1280:100:0" -c:a copy output.mp4
```

### Tăng/giảm tốc độ video
```bash
# Nhanh gấp đôi (video + audio)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" output.mp4
# Chậm còn 1 nửa
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" output.mp4
```
`atempo` chỉ nhận giá trị 0.5-2.0 mỗi lần; muốn nhanh/chậm hơn thì nối chuỗi
nhiều `atempo` lại, ví dụ x4 = `atempo=2.0,atempo=2.0`.

---

## Lưu ý chung
- Luôn kiểm tra file output bằng `ffprobe` sau khi chạy xong
- Với file lớn hoặc encode chất lượng cao, quá trình có thể mất nhiều phút — báo
  trước cho người dùng
- `-c copy` = không encode lại (nhanh, giữ chất lượng, nhưng hạn chế về điểm cắt/ghép
  chính xác). Bỏ `-c copy` và chỉ định `-c:v libx264 -c:a aac` khi cần độ chính xác
  hoặc khi ghép các file khác định dạng
