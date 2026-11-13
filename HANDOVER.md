# HANDOVER — lam-net

## Tóm tắt (cho em Minh Anh)
M1 xong phần code: app có giao diện (kéo-thả, chọn kiểu ảnh và mức phóng, thanh tiến độ, nút Dừng, xem trước/sau). Chị đã thử chạy thật trên 3 ảnh của em ở môi trường bên chị. Việc còn lại: em lấy bản mới về (`cap-nhat.bat`) rồi bấm đúp `mo-app.bat` để thử trên máy em. Không có việc gì chờ em quyết.

---
- **Cập nhật:** 2026-11-13 — phiên 3 (M1). Commit M1 do Claude đẩy thẳng lên `main` trên GitHub (xem `git log`); tag gần nhất `m0` (`d731e38`). Chưa gắn tag `m1` — gắn khi em xác nhận app chạy trên máy em.
- **Đang làm dở:** chờ em chạy thử app trên máy em.
- **Việc kế tiếp (tối đa 3):**
  1. Em chạy `cap-nhat.bat` → `mo-app.bat`, thử 1 chương; đọc `outputs/app-log.txt` (thời gian từng ảnh với ô 384) → ghi `docs/QA.md`, gắn tag `m1`.
  2. M2: xử lý hàng loạt hoàn chỉnh (app đã nhận cả thư mục; cần thêm: giữ cấu trúc thư mục con, bỏ qua ảnh đã làm, ước lượng thời gian còn lại).
  3. M3: xuất PNG/JPG/WebP, tự chia trang khi quá giới hạn định dạng, nén vừa phải cho web.
- **Đang chờ chủ dự án quyết:** không có.
- **Cấu trúc code:**
  - `src/lam_net/gui.py` — PySide6. `Worker(QThread)` chạy tuần tự, kiểm tra cờ dừng mỗi ô (ném `Cancelled` trong callback `progress`). `Preview`: hai `QGraphicsView` cùng kích thước cảnh (ảnh trước kéo giãn về kích thước ảnh sau) → đồng bộ thanh cuộn và phóng. Lỗi ghi `outputs/app-log.txt` (`sys.excepthook` + mỗi ảnh xong ghi 1 dòng có thời gian).
  - `src/lam_net/engine.py`, `tiling.py` (**lõi khóa**), `process.py`, `cli.py` — như M0; mặc định ô đổi 192 → 384 (cli + process + gui).
  - `mo-app.bat` — chưa có `.venv312` thì gọi `chay-m0.bat`; thiếu PySide6 thì `pip install -r requirements.txt`; chạy `pythonw` (không hiện cửa sổ đen).
  - `cap-nhat.bat` — `git pull --ff-only origin main`.
  - `ban-giao.bat` — bản viết cho phiên M0 (danh sách file + message cố định). Không chạy lại; phiên sau, nếu cần em commit từ máy, Claude viết bản mới.
- **Cách giao code (mới):** Claude có quyền push vào repo `anhtm01042009-del/lam-net` qua phiên làm việc → sửa trong bản clone `/home/claude/lam-net`, commit + push `main`, em chạy `cap-nhat.bat`. Dùng khi kết nối tới máy em hỏng. Trước khi push luôn `git pull` để không đè việc em làm ở máy.
- **Lưu ý / bẫy:**
  - Máy em: i5-4300U (2 nhân/4 luồng), RAM 7,7 GB, GPU Intel HD Haswell **không có Vulkan**. Luôn dùng `.venv312` (Python 3.12 64-bit) — Python mặc định của máy không có onnxruntime.
  - Kết nối tới máy em (remote-devices) hay chập chờn/timeout. App Claude **chặn tải file `.bat`** → nếu phải gửi file thì gửi đuôi `.txt` để em đổi tên (em đã bật hiện đuôi file).
  - `engine/*.onnx` không nằm trong git; máy em đã có. Máy mới tạo lại theo `engine/README.md`.
  - Repo lưu LF; máy em `core.autocrlf=true` nên cảnh báo "LF will be replaced by CRLF" là bình thường.
  - Không ghi số đo tốc độ của môi trường Claude vào tài liệu (chỉ so sánh tương đối).
- **File cần đọc trước:** `RULES.md`, `HANDOVER.md`, `src/lam_net/gui.py`.
