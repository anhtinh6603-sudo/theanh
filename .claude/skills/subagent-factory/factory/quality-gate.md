# Quality gate - đạt mới được nói "đã xong"

Kiểm trên đầu ra thật. Mỗi tiêu chí ghi `ĐẠT` / `CHƯA ĐẠT` + bằng chứng.

| # | Tiêu chí | Kiểm gì |
|---|---|---|
| 1 | Đúng yêu cầu | Đủ nội dung, đúng đối tượng, đúng phạm vi |
| 2 | Đúng thương hiệu | Tên, giọng, màu, font, logo, tuyên bố nguồn (theo `memory/profile.md`) |
| 3 | Đúng kỹ thuật | Định dạng, kích thước, codec, liên kết, file mở được không lỗi |
| 4 | Đúng quyền | Tài sản hợp lệ, không lộ dữ liệu/bí mật, không vượt quyền |
| 5 | Đúng trải nghiệm | Dễ đọc, dễ dùng, mở được, biết bước tiếp theo |
| 6 | Có bằng chứng | Preview, log, thông số (vd. output `ffprobe`) hoặc trạng thái xác nhận |

## Retry có giới hạn

Mỗi lỗi ghi: nguyên nhân → cách sửa → lần thử thứ mấy. Hết `max_retry`
(registry) thì báo đúng phần chưa đạt; không lặp vô hạn, không báo hoàn thành giả.

## Mẫu báo cáo bàn giao

```
JOB: <job_id>  |  Agent: <id>  |  Trạng thái: done/failed
Đầu ra: <đường dẫn>
Gate: 1 ✅ 2 ✅ 3 ✅ 4 ✅ 5 ✅ 6 ✅ (bằng chứng: ...)
Retry: 0/2
Bước tiếp theo / cần chủ duyệt: ...
```
