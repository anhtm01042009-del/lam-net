# RULES — Quy tắc dự án lam-net

Mỗi dòng một quy tắc, kèm ngày ghi. CHỈ THÊM; quy tắc mới mâu thuẫn dòng cũ thì hỏi em Minh Anh trước.

## Quy tắc cứng
- [2026-11-13] Mô hình AI và thư viện chỉ lấy từ nguồn chính thức; ghi nguồn + giấy phép vào `SOURCES.md` trước khi dùng.
- [2026-11-13] Không bao giờ ghi đè ảnh gốc; kết quả luôn lưu ra thư mục hoặc tên file mới.
- [2026-11-13] Phần lõi cắt–ghép ảnh dài bị khóa: chỉ sửa khi các ca trong `validation/` chạy lại vẫn đạt.
- [2026-11-13] Không đưa ảnh truyện có bản quyền, ảnh cá nhân và file mô hình lớn lên GitHub (chặn bằng `.gitignore`).
- [2026-11-13] App phải chạy được trên máy không có card đồ họa rời (CPU là đường chính); tăng tốc bằng GPU chỉ là phần thêm.
- [2026-11-13] Không ghi số liệu tốc độ hay chất lượng khi chưa đo thật trên máy; kết quả đo ghi vào `docs/QA.md`.
- [2026-11-13] Tiêu chí chất lượng: ảnh truyện đăng web phải thật nét, không vỡ.
- [2026-11-13] Mặc định phóng 2× (chạy AI 4× rồi thu về 2×) cho ảnh đăng web; 4× là tùy chọn khi cần phóng to lớn.

## Git
- [2026-11-13] Repo `lam-net` trên tài khoản GitHub của em Minh Anh; commit và push thẳng `main`, không dùng nhánh phụ; gắn tag cho mỗi mốc (`m0`, `m1`, …).
- [2026-11-13] Cập nhật code trực tiếp vào `D:\Minh-dev\lam-net`, không đóng gói zip.

## Chốt phiên
- [2026-11-13] Đầu phiên chạy `tiep-quan`: đọc `HANDOVER.md` trước, kéo bản mới nhất từ GitHub.
- [2026-11-13] Trong phiên: quyết định lâu dài ghi dần vào `RULES.md`, thay đổi sản phẩm ghi vào `CHANGELOG.md`.
- [2026-11-13] Cuối phiên chạy `ban-giao`: chạy thử/kiểm tra, ghi đè `HANDOVER.md`, thêm dòng vào `CHANGELOG.md` và `docs/QA.md`, chốt quy ước còn thiếu vào `RULES.md`, commit và push.
- [2026-11-13] Không dùng Notion; repo là nơi ghi chép duy nhất.
