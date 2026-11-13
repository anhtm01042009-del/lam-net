# validation/ — Ca kiểm chứng

Mỗi ca trong `cases/` gồm: ảnh đầu vào nhỏ (tự tạo, không có bản quyền), lệnh chạy, và tiêu chí đạt đo được.
Phần lõi cắt–ghép chỉ được sửa khi mọi ca ở đây vẫn đạt.

Ca dự kiến cho M0:
1. Ảnh dọc dài có vạch kẻ và chữ chạy qua ranh giới các đoạn → sau khi ghép không có vệt hay lệch ở chỗ nối.
2. Ảnh có chiều cao không chia hết cho kích thước đoạn → không mất hàng pixel nào ở cuối.
3. Ảnh vượt giới hạn định dạng sau khi phóng to → tự chia thành nhiều trang, ghép lại đúng ảnh gốc.
