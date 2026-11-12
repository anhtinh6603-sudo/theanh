---
name: huong-dan-edit-video-bang-ai
description: Hướng dẫn edit (dựng, chỉnh sửa) video bằng AI - cắt thô theo nội dung, tự động phụ đề tiếng Việt, cắt khoảng lặng, dựng theo bản chép lời, thêm b-roll, làm sạch âm thanh, đổi khung hình ngang sang dọc, nhịp cắt giữ người xem, chỉnh màu, làm thumbnail, và xuất đúng thông số từng nền tảng. Dùng skill này khi người dùng hỏi cách edit video bằng AI, dựng video nhanh, CapCut/Premiere/DaVinci/Descript, thêm phụ đề tự động, cắt video ngắn từ video dài, hoặc muốn video mượt và giữ chân người xem hơn - kể cả khi họ chỉ nói "video của tôi nhìn chán quá". Việc cắt/ghép/nén file trực tiếp bằng dòng lệnh thuộc skill video-editing (ffmpeg) nếu có cài.
---

# Hướng dẫn edit video bằng AI

Edit tốt là **bỏ đi những gì không cần** và **giữ nhịp**. AI giúp làm nhanh các việc cơ học (chép lời, cắt lặng, phụ đề, làm sạch âm), còn quyết định giữ gì, bỏ gì vẫn là của người dùng. Người dùng thường mới: nói từng bước bấm, nêu thuật ngữ bằng một câu (b-roll, jump cut, reframe...).

## Bước 0 - Hỏi nhanh (gộp, tối đa 5 câu)

1. Video gốc là gì (người nói trước camera, quay sản phẩm, quay màn hình, cắt từ video dài), dài bao lâu?
2. Đăng ở đâu và tỷ lệ khung hình mong muốn (dọc 9:16, ngang 16:9, vuông)?
3. Đang dùng phần mềm nào (CapCut, Premiere, DaVinci Resolve, Descript, điện thoại) hay chưa có?
4. Vấn đề chính: dài dòng, thiếu phụ đề, âm thanh kém, hình chán, hay không biết bắt đầu từ đâu?
5. Muốn phong cách nào (nhanh-năng lượng, điềm tĩnh, chuyên nghiệp, kể chuyện)?

## Quy trình 8 bước

**1. Chuẩn bị.** Gom tư liệu vào một thư mục, đặt tên rõ ràng, sao lưu bản gốc. Chọn khung hình đích ngay từ đầu để không phải làm lại.

**2. Chép lời (transcript) bằng AI.** Cho công cụ tự nhận diện lời nói tiếng Việt, rồi **đọc lại và sửa** tên riêng, thuật ngữ, số. Phụ đề sai chính tả làm video mất uy tín.

**3. Chọn nội dung và cắt thô.** Dựa vào bản chép lời để chọn ý cần giữ (nhiều công cụ cho cắt video bằng cách xóa chữ trong văn bản). Với video dài muốn cắt thành clip ngắn: tìm các đoạn có mở đầu mạnh, một ý trọn vẹn, 30-90 giây. Bỏ đoạn lạc đề, nói vấp, lặp ý.

**4. Cắt khoảng lặng và lời thừa.** Dùng tính năng tự động cắt lặng, đặt mức vừa phải: cắt quá gắt nghe như máy. Giữ một nhịp thở ngắn ở chỗ đổi ý.

**5. Nhịp và hình ảnh.** Cho video dọc: đổi hình/góc hoặc zoom nhẹ khoảng mỗi vài giây; chèn b-roll (ảnh sản phẩm, minh họa) lúc nói về việc cụ thể; thêm chữ nhấn cho từ khóa chính. Đừng lạm dụng hiệu ứng: mỗi hiệu ứng phải phục vụ ý nói.

**6. Âm thanh.** Ưu tiên làm sạch tiếng nói trước (giảm ồn, cân bằng âm lượng), rồi mới thêm nhạc nền nhỏ hơn tiếng nói rõ ràng. Nhạc phải có bản quyền hợp lệ. Nghe lại bằng tai nghe và loa điện thoại.

**7. Phụ đề và chữ trên hình.** Tự động phụ đề rồi sửa tay; tối đa 1-2 dòng, chữ lớn, độ tương phản cao, nằm trong vùng an toàn (tránh phần bị nút/tiêu đề nền tảng che). Nhấn màu ở từ khóa, không nhấn cả câu.

**8. Chỉnh màu, thumbnail, xuất.** Chỉnh màu nhẹ cho nhất quán (cân bằng trắng, độ sáng, tương phản); nếu cần thumbnail: một ý, chữ lớn ít từ, mặt/sản phẩm rõ. Xuất theo bảng dưới.

## Thông số xuất tham khảo

| Nền tảng | Khung hình | Độ phân giải | Ghi chú |
|---|---|---|---|
| TikTok / Reels / Shorts | 9:16 dọc | 1080x1920 | Định dạng H.264/MP4, âm thanh AAC |
| YouTube ngang | 16:9 | 1920x1080 (hoặc cao hơn) | Tốc độ khung hình giữ như tư liệu gốc |
| Facebook feed | 4:5 hoặc 1:1 | 1080x1350 / 1080x1080 | Phụ đề bắt buộc vì nhiều người xem không bật tiếng |

Giới hạn độ dài và dung lượng thay đổi theo nền tảng: nếu có công cụ tìm web, kiểm tra thông số hiện hành trước khi khẳng định.

## Khi người dùng cần Claude làm luôn thao tác trên file

Nếu người dùng đưa file video vào cuộc trò chuyện và môi trường có skill `video-editing` (ffmpeg) thì dùng nó để cắt/ghép/nén/thêm phụ đề trực tiếp; skill này lúc đó chỉ đóng vai hướng dẫn quyết định dựng (giữ gì, bỏ gì, nhịp thế nào). Nếu không có, giao **bảng dựng** (mốc thời gian - việc cần làm) để người dùng tự làm trong phần mềm của họ.

## Rào chắn

- Chỉ dùng tư liệu, nhạc, hình ảnh có quyền sử dụng. Không dùng giọng/gương mặt người thật để làm giả lời nói hay tin giả.
- Không dùng AI chỉnh sửa để bóp méo nội dung người khác nói (cắt ghép làm sai ý).
- Video có yếu tố do AI tạo trông như thật: gắn nhãn theo yêu cầu nền tảng.
- Chỉnh sửa hình ảnh sản phẩm không làm sai lệch chất lượng thật.

## Kiểm tra cuối

Xem hết video bằng điện thoại: 3 giây đầu có giữ được người xem? Phụ đề đúng chính tả và đọc kịp? Âm thanh rõ, không chói? Có đoạn nào có thể cắt thêm mà vẫn đủ ý? Xuất đúng khung hình và độ phân giải của nền tảng đích?
