# Hỏi & Đáp — lam-net

CHỈ THÊM. Mỗi mục ghi nguồn và độ chắc chắn: Đã kiểm chứng / Tra cứu / Giả định.

## 2026-11-13 (phiên 3)
**H:** Cỡ ô nào nhanh nhất?
**Đ:** Ô càng lớn thì phần đệm quanh ô chiếm tỉ lệ càng nhỏ nên càng nhanh: đệm 20 px quanh ô 192 làm tăng ~46% khối lượng tính, quanh ô 384 chỉ ~22%. Thử ở môi trường Claude, ô 384 nhanh hơn ô 192 rõ rệt và gần bằng ô 512. Đổi mặc định sang 384; RAM tăng không đáng kể. Số giây trên máy em cần đo lại.
*Nguồn:* đo so sánh tương đối ở môi trường Claude. *Độ chắc chắn:* Đã kiểm chứng (tương đối), chờ số đo trên máy em.

## 2026-11-13 (phiên 2)
**H:** Ghép ảnh từ nhiều ô có lộ đường nối không?
**Đ:** Không. Mỗi ô được đệm thêm phần ảnh xung quanh lớn hơn vùng ảnh hưởng của mô hình (17 lớp conv cho "truyện", 33 lớp cho "ảnh chụp"), nên ảnh ghép khớp tuyệt đối với chạy nguyên ảnh: ca `validation/cases/test_duong_noi.py` cho sai lệch tối đa 0 ở cả hai mô hình, cỡ ô 64 và 100. Kiểm tra bằng mắt trên ảnh truyện thật của em cũng không thấy vệt.
*Nguồn:* chạy ca kiểm chứng ở môi trường của Claude. *Độ chắc chắn:* Đã kiểm chứng (chờ chạy lại trên máy em qua `chay-m0.bat`).

**H:** Phóng 2× làm thế nào khi mô hình chỉ có 4×?
**Đ:** Chạy mô hình 4× rồi thu nhỏ về 2× (INTER_AREA), giống tuỳ chọn outscale của Real-ESRGAN. Vì vậy 2× tốn thời gian gần bằng 4×.
*Nguồn:* mã `process.py`. *Độ chắc chắn:* Đã kiểm chứng.

**H:** Tốc độ trên máy em thế nào?
**Đ:** Đo bằng `chay-m0.bat` (Python 3.12 64-bit, ONNX Runtime CPU, ô 192 px):
- Truyện dài 576×4322, chế độ truyện, 4×: 121 giây, RAM cao nhất ~290 MB.
- Ảnh 620×668, chế độ ảnh chụp, 4×: 49 giây, RAM ~215 MB → chế độ ảnh chụp chậm hơn chế độ truyện khoảng 2,4 lần theo diện tích.
- Chế độ nhanh (không AI), truyện dài 4×: 1,2 giây.
- 2× tốn thời gian gần như 4× (vì chạy 4× rồi thu nhỏ).
*Nguồn:* ảnh chụp màn hình cửa sổ `chay-m0.bat` em gửi. *Độ chắc chắn:* Đã kiểm chứng (một lần đo; file log chưa đọc được do mất kết nối với máy).

**H:** Mặc định 2× hay 4×?
**Đ:** 2×. Em đặt tiêu chí "đăng web phải thật nét, không vỡ"; bản 2× (rộng 1152 px với ảnh gốc 576 px) vẫn giữ nét do AI tạo ra, vừa màn hình đọc, file nhẹ hơn 4× khoảng 4 lần. 4× giữ làm tùy chọn.
*Nguồn:* quyết định của em + so sánh trực quan. *Độ chắc chắn:* Đã kiểm chứng.

## 2026-11-13
**H:** Máy của em có chạy được Real-ESRGAN-ncnn-vulkan / Upscayl không?
**Đ:** Không. Máy dùng Intel HD Graphics đời Haswell (i5-4300U); Intel không hỗ trợ Vulkan trên Windows cho thế hệ này (chỉ từ thế hệ 6 trở lên). Cả hai công cụ trên đều cần Vulkan.
*Nguồn:* Task Manager trên máy em; diễn đàn Intel Community (trả lời của nhân viên Intel về HD 4400). *Độ chắc chắn:* Tra cứu (chưa thử chạy trực tiếp).

**H:** Ảnh truyện dài phóng to có vướng giới hạn kích thước không?
**Đ:** Có thể. JPEG tối đa 65.535 px mỗi chiều; ảnh dài phóng 4× dễ vượt → cần tự chia trang khi xuất.
*Nguồn:* đặc tả định dạng JPEG. *Độ chắc chắn:* Tra cứu.
