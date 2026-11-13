# SOURCES — Nguồn và giấy phép

Mỗi mô hình/thư viện ghi: tên, nguồn chính thức, giấy phép, ngày lấy, ghi chú. Chưa có dòng ở đây thì chưa được dùng.

| Thành phần | Nguồn | Giấy phép | Ngày lấy | Ghi chú |
|---|---|---|---|---|
| Real-ESRGAN `realesr-animevideov3.pth` | https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth | BSD-3-Clause | 2026-11-13 | sha256 `b8a8376811077954…`; chuyển sang `engine/realesr-animevideov3.onnx` bằng `tools/pth_to_onnx.py` — chế độ "truyện" |
| Real-ESRGAN `realesr-general-x4v3.pth` | https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth | BSD-3-Clause | 2026-11-13 | sha256 `8dc7edb9ac80ccdc…`; chuyển sang `engine/realesr-general-x4v3.onnx` — chế độ "ảnh chụp" |
| ONNX Runtime | https://github.com/microsoft/onnxruntime | (kiểm tra khi cài) | 2026-11-13 | Chạy mô hình trên CPU |
| OpenCV | https://github.com/opencv/opencv | (kiểm tra khi cài) | 2026-11-13 | Chế độ nhanh + đổi tỉ lệ |
| PySide6 | https://pypi.org/project/PySide6/ | (kiểm tra khi cài) | — | Giao diện, dùng từ M1 |
| psutil | https://pypi.org/project/psutil/ | (kiểm tra khi cài) | 2026-11-13 | Đo RAM khi chạy `--do` |
| Pillow | https://pypi.org/project/Pillow/ | (kiểm tra khi cài) | 2026-11-13 | Đọc/ghi ảnh |
