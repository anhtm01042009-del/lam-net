# Nhật ký thay đổi — lam-net

CHỈ THÊM, không sửa dòng cũ. Viết bằng lời thường, không ghi lệnh, log hay thông tin máy.

## 2026-11-13 — M1: app có giao diện
- Mở app bằng một cú bấm đúp; kéo-thả ảnh hoặc cả thư mục vào danh sách.
- Chọn kiểu ảnh (truyện / ảnh chụp / nhanh không AI) và mức phóng (2× đăng web, 4× phóng lớn).
- Làm nét chạy ngầm, có thanh tiến độ cho từng ảnh và cả danh sách, có nút Dừng.
- Xem trước và sau cạnh nhau, cuộn và phóng to đồng bộ hai bên.
- Xử lý nhanh hơn nhờ chia ảnh thành ô lớn hơn.

## 2026-11-13 — M0: lõi làm nét chạy được
- Làm nét và phóng to ảnh 2× hoặc 4× bằng AI, chạy trên CPU, có hai chế độ: truyện/tranh vẽ và ảnh chụp.
- Ảnh truyện dài được xử lý theo từng ô nhỏ rồi ghép lại; kết quả giống hệt xử lý nguyên ảnh, không lộ đường nối, dùng ít bộ nhớ.
- Có chế độ nhanh không dùng AI.
- Mặc định phóng 2× để đăng web (ảnh vẫn nét, file nhẹ); 4× là tùy chọn.
- Ảnh gốc không bao giờ bị ghi đè; kết quả lưu riêng vào thư mục kết quả.

## 2026-11-13 — Khởi động dự án
- Tạo khung dự án: cấu trúc thư mục, quy tắc, file ghi chép.
- Chốt hướng kỹ thuật: làm nét bằng AI chạy trên CPU (máy hiện tại không hỗ trợ Vulkan), hỗ trợ ảnh truyện dài bằng cách cắt–ghép chồng lấn.
