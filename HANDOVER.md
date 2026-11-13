# HANDOVER — lam-net

## Tóm tắt (cho em Minh Anh)
M0 xong: làm nét chạy trên máy em, ảnh truyện dài ghép không lộ đường nối. Ảnh dài 576×4322 mất khoảng 2 phút, RAM dưới 300 MB. Đã chốt mặc định 2× để đăng web. Phiên sau bắt đầu M1: giao diện kéo-thả, xem trước/sau. Không có việc gì đang chờ em quyết.

---
- **Cập nhật:** 2026-11-13 — phiên 2 (M0). Commit M0 + tag `m0` được tạo bằng `ban-giao.bat` (hash: xem `git log`). Commit trước: `b635495` (khởi động).
- **Đang làm dở:** không có.
- **Việc kế tiếp (tối đa 3):**
  1. M1: giao diện PySide6 kéo-thả (ảnh/thư mục), chọn kiểu ảnh (truyện/ảnh chụp), 2×/4×, xem trước/sau; chạy xử lý trong luồng riêng để giao diện không treo, có thanh tiến độ (dùng `progress` callback của `upscale_tiled`).
  2. Tăng tốc (tuỳ chọn): thử tile 256/384 (RAM còn dư nhiều) và `onnxruntime-directml` (`Upscaler(provider="dml")` có sẵn, CLI chưa có tuỳ chọn). Đo lại bằng `chay-m0.bat`.
  3. Xác nhận dòng `KET QUA: DAT` trong `outputs/ket-qua-m0.txt` (chưa đọc được do mất kết nối; `ban-giao.bat` đã chạy lại ca này trước khi commit — commit chỉ xảy ra khi DAT).
- **Đang chờ chủ dự án quyết:** không có.
- **Số đo M0 trên máy em** (chi tiết `docs/QA.md`): truyện 4× ảnh 576×4322 = 121 s, RAM ~290 MB; ảnh chụp 4× ảnh 620×668 = 49 s; chế độ nhanh 1,2 s. 2× tốn gần bằng 4×.
- **Cấu trúc code:**
  - `src/lam_net/engine.py` — `Upscaler(kieu)`: ONNX Runtime CPU; `pad` = bán kính vùng ảnh hưởng + 2 (truyện 18+2, ảnh 34+2).
  - `src/lam_net/tiling.py` — **lõi khóa**: cắt ô + đệm, giữ phần lõi; khớp tuyệt đối với chạy nguyên ảnh.
  - `src/lam_net/process.py` — 4× rồi INTER_AREA về 2×; chế độ nhanh (Lanczos + unsharp); tên file ra không ghi đè.
  - `src/lam_net/cli.py` — mặc định `--scale 2`; `--do` in thời gian + RAM; `--log` ghi thêm vào file.
  - `tools/pth_to_onnx.py` — ONNX từ `.pth` chính thức, không cần PyTorch (SRVGGNetCompact; PixelShuffle = DepthToSpace CRD).
  - `validation/cases/test_duong_noi.py` — ca kiểm chứng đường nối.
  - `chay-m0.bat` — cài Python 3.12 64-bit + `.venv312` + thư viện, chạy kiểm chứng, đo tốc độ → `outputs/ket-qua-m0.txt`.
  - `ban-giao.bat` — chốt phiên M0, tự chứa: chạy kiểm chứng (TRUOT thì dừng), `git add` danh sách file viết sẵn trong bat, commit (message viết ra %TEMP%), pull --rebase, push, tag `m0`; nhật ký `outputs/ban-giao-log.txt`. Phiên sau Claude viết lại danh sách file/message/tag trong bat cho phiên đó.
- **Lưu ý / bẫy:**
  - Máy em: i5-4300U (2 nhân/4 luồng), RAM 7,7 GB, GPU Intel HD Haswell **không có Vulkan**.
  - Python mặc định trên máy em không có bản onnxruntime ("No matching distribution") → luôn dùng `.venv312` (Python 3.12 64-bit). Thư mục `.venv` cũ bỏ, em tự xoá khi tiện.
  - `engine/*.onnx` không nằm trong git; máy mới tạo lại theo `engine/README.md`. Môi trường Claude không tải được PyTorch (download.pytorch.org bị chặn).
  - Phiên Claude không có shell trên máy em; kết nối tới máy hay chập chờn (Service Unavailable / Bad Gateway) → sau mỗi lần ghi file kiểm tra kích thước bằng `device_list_dir`, lỗi thì đợi rồi thử lại.
  - Không ghi số đo tốc độ của môi trường Claude vào tài liệu.
  - Git: `C:\Program Files\Git\cmd\git.exe`, đã đăng nhập GitHub qua trình duyệt.
- **File cần đọc trước:** `RULES.md`, `HANDOVER.md`, `src/lam_net/tiling.py`.
