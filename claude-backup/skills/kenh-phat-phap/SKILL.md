---
name: kenh-phat-phap
description: "Dựng nội dung và video ngắn cho kênh Phật pháp tiếng Việt - viết kịch bản 30-45 giây, kiểm định chất lượng nội dung (chặn mê tín, chặn ép tương tác, chặn trích dẫn kinh điển không nguồn), vẽ ảnh nền theo khoá nhận diện, tạo giọng đọc nữ và ghép video dọc 9:16. LUÔN dùng skill này khi người dùng nhắc đến làm video Phật pháp, nội dung Phật giáo, kênh tâm linh, kịch bản thiền, hoặc kiểm tra nội dung Phật pháp trước khi đăng."
---

# Kênh Phật pháp

Dựng nội dung và video ngắn cho kênh Phật pháp tiếng Việt, từ kịch bản đến file MP4.

## Nguyên tắc gốc

Kênh Phật pháp khác kênh giải trí ở một điểm: người xem đến với tâm tin cậy.
Viết sai một câu kinh, hứa một điều không có thật, là phụ lại lòng tin đó.
Vì vậy skill này đặt kiểm định lên trước tốc độ.

**Ba điều tuyệt đối không làm:**

1. **Không bịa lời kinh.** Không viết "Đức Phật dạy rằng..." rồi tự nghĩ ra
   phần sau. Nếu không tra được nguồn, viết như suy nghĩ của mình, không gán
   cho Phật hay cho kinh.
2. **Không hứa tài lộc, vận may, chữa bệnh.** Không thuộc chánh pháp, và vi phạm
   chính sách quảng cáo sức khoẻ của các nền tảng.
3. **Không dựng hình Đức Phật hay tăng ni bằng AI.** Ảnh AI sai tướng hảo,
   sai ấn tay, thừa thiếu ngón — với người có tín tâm đó là điều thất kính.

## Quy trình

### Bước 1 — Viết nội dung

Tạo file JSON trong `noi_dung/`, theo mẫu `noi_dung/buong_bo.json`:

| Trường | Ý nghĩa |
|---|---|
| `tieu_de` | Tiêu đề video |
| `hook` | 3 giây đầu, một câu, dưới 18 từ |
| `than_bai` | Thân bài, một ý duy nhất |
| `ket` | Câu kết, không ép tương tác |
| `caption` | Caption đăng bài |
| `goi_y_thuc_hanh` | Một việc người xem làm được ngay hôm nay |
| `prompt_hinh_anh` | Danh sách cảnh nền, không được rỗng |
| `thoi_luong_giay` | Thời lượng mục tiêu |
| `nguon` | Mã nguồn kinh điển nếu có trích dẫn |

Văn nói, câu ngắn, mỗi video một ý. Không xưng "ta", không đặt mình vào
vị thế bậc thầy — kênh là người cùng học, không phải người giảng đạo.

### Bước 2 — Kiểm định (bắt buộc)

```bash
python scripts/kiem_dinh.py noi_dung/ten_bai.json
```

Phải đạt từ **95/100** và không có lỗi chặn nào. Cổng kiểm định soát:
mê tín và hứa tài lộc, ép tương tác bằng tín ngưỡng, trích dẫn kinh điển
không nguồn, giọng bậc thầy, thời lượng lệch quá 25%, thiếu phần bắt buộc,
danh sách prompt rỗng.

Mọi luật so khớp trên bản đã bỏ dấu, nên viết "chia sẻ", "chia se", hay
"CHIA SẺ" đều bị bắt như nhau.

Tự kiểm tra chính cổng kiểm định:
```bash
python scripts/kiem_dinh.py --tu-kiem-tra
```

### Bước 3 — Ảnh nền

```bash
python scripts/tao_nen.py --kieu ho_sen --seed 7
python scripts/tao_nen.py --kieu nui --seed 21
```

Vẽ bằng hình học, không qua AI tạo ảnh — nên không bao giờ sinh ra tượng Phật
sai tướng. Đổi `--seed` để ra bố cục khác.

Dùng ảnh chụp thật cũng được, chỉ cần đúng khoá nhận diện.

### Bước 4 — Giọng đọc

```bash
python scripts/make_voice.py --bai ten_bai --giong nu --toc-do -5%
```

Dùng edge-tts, miễn phí, không cần khoá API. Giọng Phật pháp nên chậm hơn
bình thường.

Không có mạng thì thêm `--offline` để dùng espeak-ng, nhưng giọng máy móc,
chỉ để thử đường ống chứ không đăng được.

### Bước 5 — Ghép video

```bash
python scripts/make_video.py --bai ten_bai --nen assets/nen_ho_sen.png
python scripts/make_video.py --bai ten_bai --nen assets/nen_nui.png --nhac assets/nhac.mp3
```

Ra `media/ten_bai/ten_bai_final.mp4` — 1080×1920, 30fps.

## Tài liệu tham khảo

- `references/brand_lock.md` — bảng màu, khung hình, vùng chữ an toàn,
  danh sách hình ảnh được và không được dùng
- `references/nguon_da_kiem.json` — danh sách nguồn kinh điển đã đối chiếu.
  **Chỉ thêm mã nguồn sau khi tự mở bản dịch và kiểm.** Không thêm chỉ vì
  AI nói rằng câu đó có trong kinh.

## Ghi chú kỹ thuật

Ba lỗi ffmpeg đã sửa, đừng đổi lại:

- Không dùng `zoompan` với ảnh tĩnh lặp — hỏng mốc thời gian, phụ đề biến mất.
  Hiệu ứng trôi dùng `crop` với biểu thức theo thời gian.
- Phụ đề đi qua file `.ass` tự sinh có khai báo `PlayResX/Y` bằng 1080×1920.
  Bộ lọc `subtitles` mặc định tính trên khung 384×288 rồi phóng to, sai hết
  cỡ chữ và lề.
- `Fontname` trong ASS phải là tên họ font (`Arial`), không phải tên file
  (`arialbd`). Sai thì libass âm thầm đổi font, có thể mất dấu tiếng Việt.
- Màu trong ASS là **BGR**: `F2E3B8` viết thành `B8E3F2`.
- Ở chế độ offline, khoảng nghỉ giữa các dòng phải chèn thành khoảng lặng thật
  trong audio, không chỉ cộng vào mốc giờ, nếu không phụ đề trôi dần.
