"""Chạy mô hình ONNX (Real-ESRGAN loại nhỏ, x4) trên CPU."""
import os
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ENGINE_DIR = ROOT / "engine"

MODELS = {
    "truyen": "realesr-animevideov3.onnx",   # truyện, tranh vẽ
    "anh": "realesr-general-x4v3.onnx",      # ảnh chụp thường
}
NATIVE_SCALE = 4
# Bán kính vùng ảnh hưởng (số lớp conv 3x3) của từng mô hình: đệm tile >= giá trị này
# thì kết quả ghép khớp tuyệt đối với chạy nguyên ảnh.
RECEPTIVE = {"truyen": 18, "anh": 34}


class Upscaler:
    def __init__(self, kieu="truyen", threads=None, provider="cpu"):
        import onnxruntime as ort
        path = ENGINE_DIR / MODELS[kieu]
        if not path.exists():
            raise FileNotFoundError(f"Chưa có mô hình: {path}")
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads or os.cpu_count() or 4
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        providers = ["CPUExecutionProvider"]
        if provider == "dml":
            providers = ["DmlExecutionProvider", "CPUExecutionProvider"]
        self.sess = ort.InferenceSession(str(path), so, providers=providers)
        self.kieu = kieu
        self.pad = RECEPTIVE[kieu] + 2

    def run(self, tile_rgb_u8: np.ndarray) -> np.ndarray:
        """tile HxWx3 uint8 -> (4H)x(4W)x3 float32 trong [0,1]."""
        x = tile_rgb_u8.astype(np.float32).transpose(2, 0, 1)[None] / 255.0
        y = self.sess.run(None, {"input": x})[0][0]
        return np.clip(y.transpose(1, 2, 0), 0.0, 1.0)
