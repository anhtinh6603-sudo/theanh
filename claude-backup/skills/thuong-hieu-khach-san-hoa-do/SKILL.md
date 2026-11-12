---
name: "thuong-hieu-khach-san-hoa-do"
description: "Bộ nhận diện và quy trình nội dung Khách sạn Hoa Đô: thông tin liên hệ, phong cách poster, giọng văn, caption mẫu, video review hằng ngày. Dùng khi làm nội dung/đăng bài cho Hoa Đô."
---

# Thương hiệu Khách sạn Hoa Đô

Bộ nhận diện và quy trình làm nội dung cho kênh của Khách sạn Hoa Đô.

## Thông tin thương hiệu

- **Tên:** Khách sạn Hoa Đô (HOA ĐÔ HOTEL)
- **Website:** https://khachsanhoado.vercel.app/
- **Facebook:** https://www.facebook.com/profile.php?id=100083118018930
- **Zalo:** 0977 600 599 — 0979 123 775
- **Kho ảnh thương hiệu (Drive):** folder id `1H0ytYBed3UCa4k2mT6pN1LCfvaSR3Cpj`
  (thư mục "Ảnh thương hiệu Hoa Đô": poster nam/nữ, ảnh phòng, sảnh, mặt tiền...)

## Phong cách hình ảnh

- Poster dọc, tone **đỏ đô + vàng gold**, chữ serif đậm.
- Ảnh có chàng trai (dòng `poster-nam-*`, `thuong-hieu-nam-*`) dùng cho video review;
  ảnh không người (dòng `hoa-do-fashion-*`) dùng khi cần khung cảnh thuần túy.
- Poster đã có sẵn tiêu đề + nút CTA "NHẮN TIN TÌM HIỂU PHÒNG".

## Giọng văn nội dung

- Thân thiện, mời gọi, xưng "mình" khi review góc nhìn khách trải nghiệm.
- Mỗi video: 5 điểm chạm (lễ tân, phòng, sảnh, sân vườn, tiện ích) + cảnh cuối đặt phòng.
- Caption luôn kèm đủ 3 kênh liên hệ: website, Facebook, Zalo.

## Quy trình sản xuất

1. **Video review hằng ngày:** xem skill `video-review-khach-san`
   (tool `~/workspace/tools/hyperframes-video/hotel_review.py`).
   Luôn dùng cờ `--endcard` với thông tin liên hệ trên.
2. **Caption mẫu khi đăng video** (thay [..] cho phù hợp):

```
🏨 KHÁCH SẠN HOA ĐÔ — [tiêu đề video]

[1-2 câu mô tả điểm nổi bật trong video]

📍 Đặt phòng ngay hôm nay!
🌐 Website: https://khachsanhoado.vercel.app/
📘 Facebook: https://www.facebook.com/profile.php?id=100083118018930
📱 Zalo: 0977 600 599 — 0979 123 775

#KhachSanHoaDo #ReviewKhachSan #DatPhong
```

Ví dụ caption đã dùng:

```
🏨 KHÁCH SẠN HOA ĐÔ — Điểm dừng chân lý tưởng cho hành trình của bạn!

✨ Phòng nghỉ rộng rãi, sạch sẽ | Sảnh đón khách ấm cúng | Lối vào xanh mát, đỗ xe dễ dàng

📍 Đặt phòng ngay hôm nay!
🌐 Website: https://khachsanhoado.vercel.app/
📘 Facebook: https://www.facebook.com/profile.php?id=100083118018930
📱 Zalo: 0977 600 599 — 0979 123 775

#KhachSanHoaDo #ReviewKhachSan #DatPhong
```

3. **Ảnh đã dùng:** tool tự ghi vào `~/workspace/hoa-do-review/used-photos.txt`,
   chế độ `--new 5` tự tránh lặp ảnh khi đăng hằng ngày.

## Lưu ý

- Không dùng ảnh/video tốn credit AI (Veo/Flow) cho nội dung hằng ngày;
  dây chuyền HyperFrames local là đủ và không giới hạn số lượng.
- Khi khách sạn có ảnh mới trên Drive, chỉ cần báo "làm video hôm nay",
  tool sẽ tự ưu tiên ảnh chưa dùng.