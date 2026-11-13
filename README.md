# lam-net — App làm nét ảnh

App máy tính (Windows) làm nét và phóng to ảnh 2×/4×, kể cả **ảnh truyện dài cuộn dọc**, chạy hoàn toàn trên máy, không cần card đồ họa rời.

- Lõi AI: Real-ESRGAN (mô hình loại nhỏ) chạy bằng ONNX Runtime trên CPU; chế độ nhanh dùng OpenCV.
- Ảnh dài: cắt thành đoạn chồng lấn → làm nét từng đoạn → ghép lại không lộ đường nối → tự chia trang khi quá giới hạn định dạng.
- Giao diện: Python + PySide6, kéo-thả.

## Thư mục
| Thư mục | Nội dung |
|---|---|
| `src/lam_net/` | Mã nguồn app |
| `engine/` | File mô hình `.onnx` (không đưa lên GitHub) |
| `validation/` | Ca kiểm chứng: ảnh mẫu nhỏ + tiêu chí đạt |
| `samples/` | Ảnh thử của em (không đưa lên GitHub) |
| `outputs/` | Ảnh kết quả (không đưa lên GitHub) |
| `docs/` | Hỏi đáp (`QA.md`) và quyết định (`decisions/`) |

## Mở app (M1)
- Bấm đúp `mo-app.bat`. Lần đầu sẽ tự cài thư viện giao diện (vài phút).
- Kéo-thả ảnh hoặc thư mục vào danh sách bên trái → chọn kiểu ảnh, mức phóng → bấm **Làm nét**. Kết quả lưu ở `outputs/` (đổi được).
- Lấy bản mới nhất từ GitHub: bấm đúp `cap-nhat.bat`.

## Chạy (M0)
- Lần đầu và mỗi khi cần đo lại: bấm đúp `chay-m0.bat` (tự cài Python + thư viện vào `.venv312`, chạy ca kiểm chứng, đo tốc độ, ghi `outputs/ket-qua-m0.txt`).
- Dòng lệnh: `.venv312\Scripts\python.exe src\lam_net\cli.py <ảnh hoặc thư mục> [--kieu truyen|anh] [--scale 2|4] [--nhanh] [--do]`

- Cuối phiên: bấm đúp `ban-giao.bat` (kiểm chứng → commit → đẩy lên GitHub → gắn tag mốc nếu có).

## File ghi chép
- `HANDOVER.md` — bàn giao giữa các phiên (ghi đè mỗi phiên).
- `CHANGELOG.md` — nhật ký thay đổi (chỉ thêm).
- `RULES.md` — quy tắc dự án (chỉ thêm).
- `SOURCES.md` — nguồn và giấy phép của mô hình, thư viện.

## Mốc
- **M0** — Script dòng lệnh: ảnh truyện dài ra không lộ đường nối + đo tốc độ thật trên máy.
- **M1** — Giao diện kéo-thả, chọn kiểu ảnh, 2×/4×, xem trước/sau.
- **M2** — Xử lý hàng loạt cả thư mục, thanh tiến độ, hủy.
- **M3** — Xuất PNG/JPG/WebP, tự chia trang, dung lượng hợp lý cho web.
- **M4** — Đóng gói `.exe`.

Không làm ở giai đoạn này: video, tự huấn luyện mô hình, bản online, xóa/dịch chữ.
