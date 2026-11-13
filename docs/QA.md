# Hỏi & Đáp — lam-net

CHỈ THÊM. Mỗi mục ghi nguồn và độ chắc chắn: Đã kiểm chứng / Tra cứu / Giả định.

## 2026-11-13
**H:** Máy của em có chạy được Real-ESRGAN-ncnn-vulkan / Upscayl không?
**Đ:** Không. Máy dùng Intel HD Graphics đời Haswell (i5-4300U); Intel không hỗ trợ Vulkan trên Windows cho thế hệ này (chỉ từ thế hệ 6 trở lên). Cả hai công cụ trên đều cần Vulkan.
*Nguồn:* Task Manager trên máy em; diễn đàn Intel Community (trả lời của nhân viên Intel về HD 4400). *Độ chắc chắn:* Tra cứu (chưa thử chạy trực tiếp).

**H:** Ảnh truyện dài phóng to có vướng giới hạn kích thước không?
**Đ:** Có thể. JPEG tối đa 65.535 px mỗi chiều; ảnh dài phóng 4× dễ vượt → cần tự chia trang khi xuất.
*Nguồn:* đặc tả định dạng JPEG. *Độ chắc chắn:* Tra cứu.
