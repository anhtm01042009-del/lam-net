"""Chuyển trọng số SRVGGNetCompact (Real-ESRGAN) từ .pth sang .onnx, không cần PyTorch.

Kiến trúc (theo realesrgan/archs/srvgg_arch.py, BSD-3-Clause):
  conv3x3(3->F) + PReLU, rồi num_conv lần [conv3x3(F->F) + PReLU],
  conv3x3(F -> 3*s*s), PixelShuffle(s), cộng với ảnh vào phóng nearest s lần.
"""
import pickle, sys, zipfile
import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper

DT = {"FloatStorage": np.float32, "HalfStorage": np.float16, "DoubleStorage": np.float64}

def load_pth(path):
    z = zipfile.ZipFile(path)
    root = z.namelist()[0].split("/")[0]

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == "_rebuild_tensor_v2":
                def rebuild(storage, offset, size, stride, *a):
                    arr = storage
                    if len(size) == 0:
                        return arr[offset].copy()
                    st = [s * arr.itemsize for s in stride]
                    return np.lib.stride_tricks.as_strided(arr[offset:], size, st).copy()
                return rebuild
            if mod == "collections" and name == "OrderedDict":
                import collections; return collections.OrderedDict
            if mod.startswith("torch") and name.endswith("Storage"):
                return name
            return super().find_class(mod, name)

        def persistent_load(self, pid):
            _, stype, key, _loc, _n = pid
            dt = DT[stype if isinstance(stype, str) else stype]
            return np.frombuffer(z.read(f"{root}/data/{key}"), dtype=dt)

    obj = U(z.open(f"{root}/data.pkl")).load()
    for k in ("params_ema", "params"):
        if isinstance(obj, dict) and k in obj:
            return obj[k]
    return obj

def build(sd, scale, out_path):
    keys = sorted({int(k.split(".")[1]) for k in sd if k.startswith("body.")})
    nodes, inits = [], []
    def init(name, arr):
        inits.append(numpy_helper.from_array(arr.astype(np.float32), name))
    cur = "input"
    for i in keys:
        w = sd[f"body.{i}.weight"]
        if w.ndim == 4:      # conv
            init(f"w{i}", w); init(f"b{i}", sd[f"body.{i}.bias"])
            nodes.append(helper.make_node("Conv", [cur, f"w{i}", f"b{i}"], [f"c{i}"], pads=[1, 1, 1, 1]))
            cur = f"c{i}"
        else:                # PReLU, slope (F,) -> (F,1,1)
            init(f"p{i}", w.reshape(-1, 1, 1))
            nodes.append(helper.make_node("PRelu", [cur, f"p{i}"], [f"a{i}"]))
            cur = f"a{i}"
    nodes.append(helper.make_node("DepthToSpace", [cur], ["up"], blocksize=scale, mode="CRD"))
    init("scales", np.array([1, 1, scale, scale], np.float32))
    nodes.append(helper.make_node("Resize", ["input", "", "scales"], ["base"], mode="nearest"))
    nodes.append(helper.make_node("Add", ["up", "base"], ["output"]))
    g = helper.make_graph(nodes, "srvgg_compact",
        [helper.make_tensor_value_info("input", TensorProto.FLOAT, [1, 3, "h", "w"])],
        [helper.make_tensor_value_info("output", TensorProto.FLOAT, [1, 3, "H", "W"])], inits)
    m = helper.make_model(g, opset_imports=[helper.make_opsetid("", 17)])
    m.ir_version = 8
    onnx.checker.check_model(m)
    onnx.save(m, out_path)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    sd = load_pth(src)
    build(sd, 4, dst)
    print("OK", dst, len(sd), "tensors")
