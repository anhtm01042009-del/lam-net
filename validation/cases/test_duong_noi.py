"""Ca kiểm chứng lõi cắt–ghép (chạy: python validation/cases/test_duong_noi.py).

Tạo ảnh tổng hợp (không bản quyền) có vạch kẻ, chữ và gradient chạy qua ranh giới ô,
kích thước không chia hết cho cỡ ô. Đạt khi:
  1. Ảnh ghép từ ô khớp với chạy nguyên ảnh: sai lệch tối đa <= 1 mức xám (làm tròn).
  2. Đúng kích thước đầu ra (không mất hàng/cột pixel).
"""
import sys
from pathlib import Path
import numpy as np
import cv2

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from lam_net.engine import Upscaler  # noqa: E402
from lam_net.tiling import upscale_tiled  # noqa: E402


def make_image(h=437, w=203):
    rng = np.random.default_rng(0)
    img = np.zeros((h, w, 3), np.uint8)
    img[:] = np.linspace(40, 220, w, dtype=np.uint8)[None, :, None]
    for y in range(0, h, 23):
        cv2.line(img, (0, y), (w, y + 40), (20, 20, 20), 1)
    for i, y in enumerate(range(30, h, 64)):
        cv2.putText(img, f"LAM NET {i}", (5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 30, 30), 1)
    noise = rng.integers(-8, 9, img.shape)
    return np.clip(img.astype(int) + noise, 0, 255).astype(np.uint8)


def main():
    ok = True
    img = make_image()
    for kieu in ("truyen", "anh"):
        up = Upscaler(kieu)
        full = (up.run(img) * 255.0 + 0.5).astype(np.uint8)
        for tile in (64, 100):
            tiled = upscale_tiled(img, up.run, 4, up.pad, tile)
            shape_ok = tiled.shape == (img.shape[0] * 4, img.shape[1] * 4, 3)
            diff = int(np.abs(tiled.astype(int) - full.astype(int)).max())
            passed = shape_ok and diff <= 1
            ok &= passed
            print(f"[{'DAT' if passed else 'TRUOT'}] {kieu} tile={tile}: kich thuoc {'dung' if shape_ok else 'SAI'}, sai lech toi da = {diff}")
    print("KET QUA:", "DAT" if ok else "TRUOT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
