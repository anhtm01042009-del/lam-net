# HANDOVER — lam-net

## Tóm tắt (cho em Minh Anh)
Đã tạo xong khung dự án, chưa có code chạy được. Việc tiếp theo là làm M0: script làm nét 1 ảnh truyện dài và đo tốc độ trên máy em. Cần em: tạo repo GitHub `lam-net` (nếu chưa) và chép vào `samples/` 2–3 ảnh thử (1 ảnh chụp, 1 ảnh truyện dài).

---
- **Cập nhật:** 2026-11-13 — phiên khởi động. Chưa có commit/tag.
- **Đang làm dở:** chưa có.
- **Việc kế tiếp (tối đa 3):**
  1. Chốt nguồn mô hình ONNX cho `realesr-animevideov3` và `realesr-general-x4v3` (bản `.pth` chính thức ở repo Real-ESRGAN; tự convert sang ONNX hay dùng bản ONNX có sẵn — ghi vào `SOURCES.md`).
  2. Viết `src/lam_net/tiling.py` (cắt đoạn chồng lấn + ghép trộn biên) và `src/lam_net/cli.py`; ca kiểm chứng đầu tiên trong `validation/cases/`.
  3. Đo tốc độ và RAM trên máy em với ảnh thật; ghi kết quả vào `docs/QA.md`.
- **Đang chờ chủ dự án quyết:** mặc định 2× hay 4× (quyết sau khi có số đo M0).
- **Lưu ý / bẫy:**
  - Máy: i5-4300U (2 nhân/4 luồng), RAM 7,7 GB (lúc kiểm tra đã dùng ~68%), GPU Intel HD Graphics đời Haswell → **không có Vulkan trên Windows** → Real-ESRGAN-ncnn-vulkan và Upscayl không chạy. Dùng ONNX Runtime CPU; DirectML chỉ thử như phần thêm.
  - Ô xử lý (tile) để nhỏ (~128–256 px) vì RAM trống ít.
  - Giới hạn kích thước định dạng: JPEG tối đa 65.535 px mỗi chiều → ảnh dài phóng 4× có thể vượt, cần chia trang khi xuất.
  - Phiên Claude không có shell trên máy em: git phải chạy bằng tay ở máy em (lệnh trong README hoặc phiên chat).
- **File cần đọc trước:** `RULES.md`, `docs/decisions/0001-loi-ai-cpu-onnx.md`, `HANDOVER.md`.
