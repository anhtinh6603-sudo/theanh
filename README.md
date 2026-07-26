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

## Build ra file APK cài trực tiếp lên điện thoại (không cần máy tính)

Repo này có sẵn GitHub Actions (`.github/workflows/build-android.yml`) tự động build file `.apk` mỗi khi có commit mới trên nhánh `claude/video-image-generation-mobile-app-fzxokv`. Trên điện thoại:

1. Mở repo trên GitHub bằng trình duyệt, vào tab **Actions**.
2. Chọn lần chạy mới nhất của workflow **Build Android APK** (đợi tới khi có dấu ✅, khoảng 5-10 phút).
3. Cuộn xuống mục **Artifacts**, tải file `anh-thanh-video-apk` (là file `.zip` chứa `app-release.apk`).
4. Giải nén và mở file `.apk` để cài — nhớ bật "Cho phép cài từ nguồn không xác định" nếu Android hỏi.

Đây là bản release build, code JS đã được đóng gói sẵn vào file APK nên chạy độc lập — không cần Metro, không cần máy tính, không cần tài khoản Expo.

## Build ra file APK bằng máy tính (tùy chọn)

Chạy các lệnh dưới đây **trên máy tính có mạng internet bình thường** (không chạy được trong môi trường build đám mây bị chặn mạng):

```bash
npm install -g eas-cli
eas login          # tạo tài khoản Expo miễn phí nếu chưa có
eas build --platform android --profile preview
```

Sau khi build xong (thường 10-15 phút), EAS sẽ đưa ra một đường link tải file `.apk`. Mở link đó **ngay trên trình duyệt điện thoại** (hoặc quét mã QR mà lệnh trên hiển thị) để tải và cài trực tiếp — nhớ bật "Cho phép cài từ nguồn không xác định" nếu Android hỏi. Không cần Expo Go, không cần giữ máy tính chạy sau khi cài xong.

Cấu hình build đã có sẵn trong `eas.json` (profile `preview` build ra `.apk`), bạn chỉ cần chạy lệnh ở trên.

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
