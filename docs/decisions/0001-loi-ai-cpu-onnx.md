# ADR 0001 — Lõi AI chạy trên CPU bằng ONNX Runtime

- **Ngày:** 2026-11-13
- **Trạng thái:** Đã chọn

## Bối cảnh
Máy của em Minh Anh không có card rời; GPU Intel HD Graphics (Haswell) không hỗ trợ Vulkan trên Windows. Real-ESRGAN-ncnn-vulkan và Upscayl (dựa trên nó) cần Vulkan.

## Quyết định
- Dùng mô hình loại nhỏ của Real-ESRGAN (`realesr-animevideov3` cho truyện, `realesr-general-x4v3` cho ảnh chụp), chạy bằng ONNX Runtime trên CPU.
- Có chế độ nhanh bằng OpenCV (kém nét hơn, gần như tức thì).
- Tự viết phần cắt–ghép ảnh dài (đoạn chồng lấn + trộn biên) và chia trang khi xuất.
- Thử DirectML để tăng tốc bằng GPU Intel như phần thêm, không phụ thuộc vào nó.

## Phương án đã loại
- Fork Upscayl: cần Vulkan, Electron nặng, ràng buộc AGPL-3.0.
- Mô hình lớn (anime_6B, x4plus) trên CPU: dự kiến quá chậm với CPU 2 nhân (sẽ xác nhận bằng số đo nếu cần).

## Hệ quả
- Tốc độ phụ thuộc CPU; phải đo ở M0 trước khi chốt mặc định 2× hay 4×.
- Kích thước ô xử lý nhỏ để vừa RAM.
