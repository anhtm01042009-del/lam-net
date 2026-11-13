"""Lõi cắt–ghép (KHÓA: chỉ sửa khi các ca trong validation/ vẫn đạt).

Mỗi ô được cắt kèm phần đệm >= bán kính vùng ảnh hưởng của mô hình, chạy mô hình,
rồi chỉ giữ phần lõi của ô. Vì vậy ảnh ghép khớp với kết quả chạy nguyên ảnh,
không có đường nối, và bộ nhớ chỉ phụ thuộc kích thước ô chứ không phụ thuộc độ dài ảnh.
"""
import numpy as np


def tiles(h, w, tile):
    for y0 in range(0, h, tile):
        for x0 in range(0, w, tile):
            yield y0, x0, min(y0 + tile, h), min(x0 + tile, w)


def upscale_tiled(img_u8, run, scale, pad, tile=192, progress=None):
    """img_u8: HxWx3 uint8. run: ô uint8 -> ô x scale float [0,1]. Trả về uint8."""
    h, w = img_u8.shape[:2]
    out = np.empty((h * scale, w * scale, 3), np.uint8)
    all_tiles = list(tiles(h, w, tile))
    for i, (y0, x0, y1, x1) in enumerate(all_tiles):
        py0, px0 = max(y0 - pad, 0), max(x0 - pad, 0)
        py1, px1 = min(y1 + pad, h), min(x1 + pad, w)
        res = run(img_u8[py0:py1, px0:px1])
        cy, cx = (y0 - py0) * scale, (x0 - px0) * scale
        core = res[cy:cy + (y1 - y0) * scale, cx:cx + (x1 - x0) * scale]
        out[y0 * scale:y1 * scale, x0 * scale:x1 * scale] = (core * 255.0 + 0.5).astype(np.uint8)
        if progress:
            progress(i + 1, len(all_tiles))
    return out
