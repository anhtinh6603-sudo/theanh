---
name: thuong-hieu-ca-nhan
description: Dùng khi người dùng muốn tạo bộ ảnh thương hiệu cá nhân đồng nhất, chèn tiêu đề hoặc badge lên ảnh Facebook/Instagram, hoặc xây dây chuyền xử lý ảnh lặp lại bằng ComfyUI. Ưu tiên công cụ tạo ảnh sẵn có cho vài ảnh; chỉ dùng ComfyUI khi cần kiểm soát chặt hay xử lý hàng loạt.
---

# Xưởng ảnh thương hiệu cá nhân

Giữ nguyên ý định, nhận diện và ảnh gốc của người dùng. Skill chỉ tạo tệp ảnh, không tự đăng mạng xã hội.

## Chọn cách làm

- Vài ảnh cần nhanh: dùng công cụ tạo/chỉnh ảnh sẵn có.
- Quy trình nhiều bước, lặp lại hoặc hàng loạt: dùng ComfyUI nếu có thể truy cập máy chạy nó.
- Chỉ chèn chữ/badge: dùng `scripts/branded_overlay.py`; không cần ComfyUI hoặc GPU.
- Không có quyền truy cập máy người dùng: hướng dẫn từng bước, không nói rằng đã chạy phần mềm trên máy họ.

## Bộ ảnh nhất quán

1. Từ ảnh tham chiếu và yêu cầu, tạo một mô tả gốc cố định: danh tính/khuôn mặt, tóc, trang phục chủ đạo, tông màu, ánh sáng và phong cách.
2. Giữ nguyên mô tả gốc ở mọi ảnh; chỉ đổi góc máy, cỡ cảnh, tư thế, hành động hoặc bối cảnh được phép.
3. Dùng ảnh neo hoặc kết quả tốt nhất làm tham chiếu cho ảnh sau. Không tuyên bố giữ khuôn mặt tuyệt đối nếu công cụ không bảo đảm.
4. So ảnh mới với ảnh neo trước khi giao; tạo lại nếu đặc điểm khóa bị lệch.

## ComfyUI

Trước khi cam kết, kiểm tra `python --version` và, nếu phù hợp, `nvidia-smi`. NVIDIA 6 GB VRAM trở lên thuận lợi; 4 GB cần mô hình nhẹ/low-VRAM; không có NVIDIA thường rất chậm.

Chỉ cài khi người dùng yêu cầu và máy đích phù hợp:

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
python -m venv mt-comfy
source mt-comfy/bin/activate  # macOS/Linux
pip install -r requirements.txt
python main.py
```

Windows kích hoạt bằng `mt-comfy\Scripts\activate`. Giao diện mặc định: `http://127.0.0.1:8188`.

ComfyUI mới cài chưa có checkpoint. Hướng dẫn lấy mô hình hợp pháp từ nguồn tin cậy, đặt `.safetensors` vào `ComfyUI/models/checkpoints/`, rồi Refresh/khởi động lại. Với chân dung có thể cân nhắc SDXL Base, Juggernaut XL hoặc RealVisXL tùy giấy phép, phần cứng và workflow.

Khi dùng workflow:

- `Load Checkpoint` phải trỏ đúng mô hình hiện có.
- Node đỏ thường do thiếu custom node; xác minh nguồn trước khi cài.
- API `/prompt` cần bản `Save (API Format)`, không phải JSON giao diện.
- Cố định seed và phần mô tả phong cách khi cần lặp bố cục.
- Làm một ảnh thử, xin duyệt rồi mới chạy hàng loạt.
- Không ghi đè ảnh gốc; xuất tệp/thư mục mới và báo đường dẫn.

Với khuôn mặt người thật, chỉ dùng ảnh có quyền sử dụng. LoRA riêng thường cần 15–20 ảnh phù hợp và thời gian huấn luyện; không hứa kết quả tức thì.

## Chèn tiêu đề và badge

Trước lần đầu trong phiên, hỏi gọn: chữ badge (có thể bỏ) và màu nhấn hex (mặc định `#FF5C8A`). Nếu người dùng đưa bài dài chưa có tiêu đề, tự rút hook 6–9 từ; ưu tiên số liệu, hook mở đầu hoặc bài học chính. Bọc đúng một cụm cần nhấn trong `**...**`.

```bash
python scripts/branded_overlay.py \
  --photo "anh-goc.jpg" \
  --headline "Bạn không cần code để **xây AI agent**" \
  --output "anh-da-chen-chu.jpg" \
  --badge "trungkienai" \
  --accent "#FF5C8A"
```

Mặc định xuất 1080×1350 (4:5), chữ trắng đậm, một cụm màu nhấn và badge góc dưới phải. Bỏ `--badge` nếu không dùng. Cần Pillow: `python -m pip install Pillow`.

Sau khi chạy, mở ảnh kiểm tra: dấu tiếng Việt, tương phản, ngắt dòng, chữ không đè badge và chủ thể không bị crop sai. Nói rõ câu đã chọn và cụm được tô màu.

## Lỗi thường gặp

- `torch.cuda.OutOfMemoryError`: giảm kích thước/batch hoặc dùng `--lowvram`; `--novram` chậm hơn.
- Queue không chạy: xem log terminal ComfyUI.
- Ảnh đen: kiểm tra workflow và checkpoint cùng họ mô hình (SDXL/SD1.5).
- `ModuleNotFoundError: PIL`: cài Pillow.
- Chữ thành ô vuông: dùng font hỗ trợ tiếng Việt như Lato/DejaVu Sans.
- Chữ đè badge: rút headline hoặc giảm cỡ chữ.

Nguồn gốc: Skill `thuong-hieu-ca-nhan` do người dùng cung cấp từ theskill.vercel.app, mã `SKW-BCHC-GK64-5ANG`; bản đóng gói này bổ sung script overlay còn thiếu trong nguồn Markdown.
