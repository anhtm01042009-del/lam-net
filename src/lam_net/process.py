"""Quy trình làm nét một ảnh: đọc -> làm nét -> đổi về tỉ lệ cần -> lưu (không ghi đè)."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

from .engine import Upscaler, NATIVE_SCALE
from .tiling import upscale_tiled


def read_rgb(path):
    with Image.open(path) as im:
        return np.asarray(im.convert("RGB"))


def safe_out_path(src, out_dir, scale, kieu):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / f"{Path(src).stem}_{kieu}_x{scale}.png"
    p, n = base, 1
    while p.exists() or p.resolve() == Path(src).resolve():
        p = base.with_name(f"{base.stem}_{n}.png"); n += 1
    return p


def fast_upscale(img, scale):
    """Chế độ nhanh: Lanczos + làm sắc nhẹ, không dùng AI."""
    h, w = img.shape[:2]
    up = cv2.resize(img, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)
    blur = cv2.GaussianBlur(up, (0, 0), 1.0)
    return cv2.addWeighted(up, 1.5, blur, -0.5, 0)


def upscale_image(img, scale=2, kieu="truyen", tile=192, upscaler=None, progress=None, nhanh=False):
    if nhanh:
        return fast_upscale(img, scale)
    up = upscaler or Upscaler(kieu)
    out = upscale_tiled(img, up.run, NATIVE_SCALE, up.pad, tile, progress)
    if scale != NATIVE_SCALE:
        h, w = img.shape[:2]
        out = cv2.resize(out, (w * scale, h * scale), interpolation=cv2.INTER_AREA)
    return out


def save_png(img, path):
    Image.fromarray(img).save(path, optimize=False)
