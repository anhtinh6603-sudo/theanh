---
name: video-editing
description: "Chỉnh sửa video bằng ffmpeg - cắt/ghép clip, đổi định dạng/nén/đổi độ phân giải, thêm phụ đề hoặc chữ overlay, tách/ghép âm thanh và nhạc nền, tạo GIF từ video, xoay/lật/crop, tăng giảm tốc độ. LUÔN dùng skill này bất cứ khi nào người dùng nhắc đến chỉnh sửa video, cắt video, ghép video, convert video, nén video, thêm phụ đề, trích xuất âm thanh, tạo GIF, hoặc thao tác với file .mp4/.mov/.avi/.mkv/.webm, kể cả khi họ không dùng từ 'edit video' trực tiếp (ví dụ: 'làm video này nhẹ hơn', 'cắt đoạn 10 giây đầu', 'gộp mấy cái video lại', 'video này sao cho có phụ đề')."
---

# Video Editing (ffmpeg)

Skill này giúp Claude Code thực hiện các thao tác chỉnh sửa video bằng ffmpeg
chạy qua bash, không cần phần mềm edit video đồ họa.

## Bước 0: Kiểm tra ffmpeg đã cài chưa

Luôn chạy trước khi làm bất kỳ thao tác nào:

```bash
ffmpeg -version
```

Nếu báo lỗi "command not found":
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt update && sudo apt install -y ffmpeg`
- Windows (PowerShell, cần Chocolatey): `choco install ffmpeg`
  hoặc hướng người dùng tải từ https://ffmpeg.org/download.html và thêm vào PATH

Nếu không có quyền cài (môi trường hạn chế), báo cho người dùng biết thay vì
cố cài bằng cách khác.

## Bước 1: Xác định rõ yêu cầu trước khi chạy lệnh

Trước khi viết lệnh ffmpeg, xác nhận với người dùng (hoặc suy luận hợp lý từ ngữ cảnh):
- File đầu vào ở đâu, định dạng gì
- Kết quả mong muốn: định dạng, thời lượng cắt, độ phân giải, chất lượng
- Có ghi đè file gốc không, hay xuất file mới (**mặc định luôn xuất file mới**,
  không ghi đè file gốc trừ khi được yêu cầu rõ ràng)

## Bước 2: Chọn recipe phù hợp

File `references/ffmpeg-cookbook.md` chứa các lệnh ffmpeg đầy đủ, phân loại theo
tác vụ: cắt/ghép, đổi định dạng/nén, phụ đề & chữ, âm thanh, GIF, xoay/crop/tốc độ.

**Luôn đọc file cookbook trước khi soạn lệnh** thay vì tự nhớ cú pháp ffmpeg,
vì cờ (flags) rất dễ nhầm giữa các phiên bản và trường hợp dùng.

## Bước 3: Chạy và kiểm tra kết quả

- Sau khi chạy lệnh, dùng `ffprobe` để kiểm tra file output có hợp lệ:
  ```bash
  ffprobe -v error -show_format -show_streams output.mp4
  ```
- Báo cho người dùng: đường dẫn file kết quả, thời lượng, dung lượng, độ phân giải
- Nếu lệnh chạy lâu (nén video lớn, convert 4K...), báo trước cho người dùng là
  có thể mất vài phút tùy cấu hình máy, đừng để họ chờ không biết chuyện gì

## Nguyên tắc an toàn khi thao tác file

- Không bao giờ ghi đè file gốc của người dùng trừ khi họ yêu cầu rõ ràng
- Với thao tác hàng loạt (batch) nhiều file, liệt kê danh sách file sẽ xử lý và
  xác nhận trước khi chạy, đặc biệt nếu là lệnh xóa hoặc ghi đè
- Luôn xuất ra thư mục output riêng (ví dụ `output/` hoặc `edited/`) thay vì lẫn
  vào thư mục chứa file gốc, trừ khi người dùng chỉ định khác

## Khi ffmpeg không đủ (yêu cầu phức tạp)

Với các yêu cầu edit phức tạp hơn (transition mượt giữa nhiều clip, color
grading nâng cao, motion tracking, hiệu ứng phức tạp), ffmpeg vẫn làm được
nhưng lệnh sẽ dài và khó đọc. Trong trường hợp đó:
1. Chia nhỏ thành các bước ffmpeg tuần tự, xử lý file trung gian
2. Giải thích rõ cho người dùng biết đây là edit nâng cao, quá trình có thể
   cần vài lần thử để đúng ý (ví dụ căn thời điểm transition)
