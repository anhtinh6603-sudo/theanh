# Ảnh Thành Video

Ứng dụng di động (Expo / React Native) biến một tấm ảnh thành video ngắn bằng AI. Chọn ảnh, mô tả chuyển động mong muốn, và nhận về video để lưu hoặc chia sẻ.

## Chạy trên điện thoại

1. Cài đặt dependencies:
   ```bash
   npm install
   ```
2. Khởi động server phát triển:
   ```bash
   npm start
   ```
3. Cài ứng dụng **Expo Go** trên điện thoại (App Store / Google Play), rồi quét mã QR hiện trên terminal/trình duyệt để mở app trực tiếp trên máy — không cần build.

Muốn build ra file cài đặt thật (APK/IPA) để dùng offline hoặc đăng lên store, dùng [EAS Build](https://docs.expo.dev/build/introduction/):
```bash
npx eas build --platform android
```

## Chế độ tạo video

Ứng dụng có 2 chế độ, chọn tự động dựa trên **Cài đặt** trong app:

- **Chế độ demo** (mặc định, không cần API key): trả về một video mẫu để bạn xem trước toàn bộ luồng thao tác.
- **Chế độ thật**: vào mục ⚙️ Cài đặt trong app, nhập:
  - **Replicate API Token** (tạo tại https://replicate.com/account/api-tokens)
  - **Model** — tên model image-to-video trên Replicate (mặc định gợi ý `minimax/video-01`)
  - **Tên trường ảnh đầu vào** / **Tên trường mô tả** — khớp với input schema của model đã chọn (xem trang model đó trên Replicate để biết tên chính xác)

Ứng dụng gọi thẳng Replicate REST API từ điện thoại, không cần server riêng.

## Cấu trúc mã nguồn

- `src/screens` — Home (danh sách dự án), Create (chọn ảnh + mô tả), Result (tiến trình tạo video, xem/lưu/chia sẻ), Settings.
- `src/lib/videoGenerator.ts` — gọi Replicate API hoặc mock, theo dõi tiến trình, hỗ trợ hủy.
- `src/lib/storage.ts` — lưu lịch sử dự án (AsyncStorage) và cài đặt/API key (SecureStore).
