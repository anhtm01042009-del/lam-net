# engine/

Đặt file mô hình `.onnx` ở đây. Thư mục này không đưa lên GitHub (trừ file này).
Nguồn từng mô hình phải ghi trong `SOURCES.md` trước khi dùng.

Cần có:
- `realesr-animevideov3.onnx` (chế độ truyện)
- `realesr-general-x4v3.onnx` (chế độ ảnh chụp)

Tạo lại khi thiếu (vd máy mới clone repo): tải 2 file `.pth` theo link trong `SOURCES.md`, rồi chạy
`python tools/pth_to_onnx.py <file.pth> engine/<ten>.onnx` (cần thêm gói `onnx`, không cần PyTorch).
