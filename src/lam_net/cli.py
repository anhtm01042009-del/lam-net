"""Dòng lệnh M0.

  python -m lam_net.cli <ảnh hoặc thư mục>... [--kieu truyen|anh] [--scale 2|4]
                        [--tile 192] [--out outputs] [--nhanh] [--do]
"""
import argparse, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lam_net.engine import Upscaler, ROOT  # noqa: E402
from lam_net.process import read_rgb, upscale_image, safe_out_path, save_png  # noqa: E402

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def collect(paths):
    for p in map(Path, paths):
        if p.is_dir():
            yield from sorted(f for f in p.iterdir() if f.suffix.lower() in EXTS)
        elif p.suffix.lower() in EXTS:
            yield p


def ram_mb():
    try:
        import psutil
        return psutil.Process(os.getpid()).memory_info().rss / 2**20
    except Exception:
        return float("nan")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Làm nét ảnh (lam-net M0)")
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--kieu", choices=["truyen", "anh"], default="truyen")
    ap.add_argument("--scale", type=int, choices=[2, 4], default=2)
    ap.add_argument("--tile", type=int, default=192)
    ap.add_argument("--out", default=str(ROOT / "outputs"))
    ap.add_argument("--nhanh", action="store_true", help="Lanczos, không dùng AI")
    ap.add_argument("--do", action="store_true", help="in thời gian và RAM")
    ap.add_argument("--log", help="ghi thêm kết quả vào file này")
    a = ap.parse_args(argv)

    def say(msg):
        print(msg, flush=True)
        if a.log:
            with open(a.log, "a", encoding="utf-8") as fh:
                fh.write(msg + "\n")

    files = list(collect(a.inputs))
    if not files:
        say("Khong tim thay anh."); return 1
    up = None if a.nhanh else Upscaler(a.kieu)
    say(f"--- kieu={'nhanh' if a.nhanh else a.kieu} scale={a.scale} tile={a.tile} ---")
    peak = ram_mb()
    for f in files:
        img = read_rgb(f)
        t0 = time.perf_counter()
        last = [0]
        def prog(i, n):
            nonlocal peak
            peak = max(peak, ram_mb())
            pct = i * 100 // n
            if pct >= last[0] + 10 or i == n:
                last[0] = pct; print(f"  {f.name}: {pct}%", flush=True)
        out = upscale_image(img, a.scale, a.kieu, a.tile, up, prog, a.nhanh)
        dt = time.perf_counter() - t0
        dst = safe_out_path(f, a.out, a.scale, "nhanh" if a.nhanh else a.kieu)
        save_png(out, dst)
        peak = max(peak, ram_mb())
        msg = f"{f.name} {img.shape[1]}x{img.shape[0]} -> {out.shape[1]}x{out.shape[0]}  => {dst.name}"
        if a.do:
            msg += f"  | {dt:.1f} s | RAM cao nhat ~{peak:.0f} MB"
        say(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
