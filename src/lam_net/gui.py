"""Giao diện Làm Nét (M1): kéo-thả ảnh, làm nét chạy ngầm, xem trước/sau.

Chạy: .venv312\\Scripts\\pythonw.exe src\\lam_net\\gui.py   (hoặc bấm đúp mo-app.bat)
"""
import os
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import PySide6  # noqa: F401
except Exception:
    import traceback as _tb
    _log = Path(__file__).resolve().parents[2] / "outputs" / "app-log.txt"
    _log.parent.mkdir(parents=True, exist_ok=True)
    _log.open("a", encoding="utf-8").write("IMPORT PySide6 LOI\n" + _tb.format_exc())
    raise

from PySide6.QtCore import Qt, QThread, Signal, QUrl, QRectF
from PySide6.QtGui import QImage, QPixmap, QDesktopServices, QPainter, QColor, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QComboBox, QProgressBar, QFileDialog,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSplitter, QMessageBox,
    QFrame, QAbstractItemView,
)

from lam_net.engine import Upscaler, ROOT
from lam_net.process import read_rgb, upscale_image, safe_out_path, save_png

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
DEFAULT_TILE = 384
KIEU = [("Truyện / tranh vẽ", "truyen"), ("Ảnh chụp", "anh"), ("Nhanh (không AI)", "nhanh")]
LOG_PATH = ROOT / "outputs" / "app-log.txt"


def log(msg):
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
    except Exception:
        pass


def np_to_qimage(arr):
    h, w = arr.shape[:2]
    arr = arr.copy(order="C")
    return QImage(arr.data, w, h, 3 * w, QImage.Format_RGB888).copy()


class Cancelled(Exception):
    pass


class Worker(QThread):
    file_started = Signal(int)
    progress = Signal(int, int, int)          # file idx, done tiles, total tiles
    file_done = Signal(int, str, float)       # file idx, out path, seconds
    file_failed = Signal(int, str)
    finished_all = Signal(bool)               # True nếu bị dừng

    def __init__(self, jobs, kieu, scale, out_dir):
        super().__init__()
        self.jobs, self.kieu, self.scale, self.out_dir = jobs, kieu, scale, out_dir
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        up = None
        nhanh = self.kieu == "nhanh"
        try:
            if not nhanh:
                up = Upscaler(self.kieu)
        except Exception as e:
            for idx, _ in self.jobs:
                self.file_failed.emit(idx, f"Không nạp được mô hình: {e}")
            self.finished_all.emit(False)
            return
        for idx, path in self.jobs:
            if self._stop:
                break
            self.file_started.emit(idx)
            t0 = time.perf_counter()
            try:
                img = read_rgb(path)

                def prog(i, n, idx=idx):
                    if self._stop:
                        raise Cancelled()
                    self.progress.emit(idx, i, n)

                out = upscale_image(img, self.scale, "truyen" if nhanh else self.kieu,
                                    DEFAULT_TILE, up, prog, nhanh)
                dst = safe_out_path(path, self.out_dir, self.scale, self.kieu)
                save_png(out, dst)
                dt = time.perf_counter() - t0
                log(f"OK {Path(path).name} {img.shape[1]}x{img.shape[0]} kieu={self.kieu} x{self.scale} {dt:.1f}s -> {dst.name}")
                self.file_done.emit(idx, str(dst), dt)
            except Cancelled:
                break
            except Exception as e:
                log("LOI " + str(path) + "\n" + traceback.format_exc())
                self.file_failed.emit(idx, str(e))
        self.finished_all.emit(self._stop)


class SyncView(QGraphicsView):
    """Khung xem ảnh: cuộn chuột để lăn, Ctrl + cuộn để phóng to/thu nhỏ."""
    zoomed = Signal(float)

    def __init__(self, title):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.item = QGraphicsPixmapItem()
        self.item.setTransformationMode(Qt.SmoothTransformation)
        self.scene().addItem(self.item)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setBackgroundBrush(QColor("#1e1e1e"))
        self.setFrameShape(QFrame.NoFrame)
        self.title = title

    def set_image(self, qimg, logical_size):
        """Hiện ảnh, kéo giãn về logical_size (w, h) để hai bên khớp toạ độ."""
        self.item.setPixmap(QPixmap.fromImage(qimg))
        sx = logical_size[0] / max(qimg.width(), 1)
        self.item.setScale(sx)
        self.scene().setSceneRect(QRectF(0, 0, logical_size[0], logical_size[1]))

    def clear_image(self):
        self.item.setPixmap(QPixmap())

    def wheelEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            f = 1.25 if e.angleDelta().y() > 0 else 0.8
            self.zoomed.emit(f)
        else:
            super().wheelEvent(e)

    def drawForeground(self, painter, rect):
        painter.save()
        painter.resetTransform()
        painter.setPen(QColor(255, 255, 255, 220))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.fillRect(8, 8, 150, 24, QColor(0, 0, 0, 140))
        painter.drawText(16, 25, self.title)
        painter.restore()


class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.before = SyncView("Trước")
        self.after = SyncView("Sau (làm nét)")
        self.info = QLabel("Chọn một ảnh đã làm nét để xem trước / sau.")
        self.info.setStyleSheet("color:#aaa; padding:4px;")
        btn_fit = QPushButton("Vừa khung")
        btn_100 = QPushButton("100%")
        btn_fit.clicked.connect(self.fit)
        btn_100.clicked.connect(self.actual)
        bar = QHBoxLayout()
        bar.addWidget(self.info, 1)
        bar.addWidget(QLabel("Ctrl + lăn chuột để phóng"))
        bar.addWidget(btn_fit)
        bar.addWidget(btn_100)
        views = QSplitter(Qt.Horizontal)
        views.addWidget(self.before)
        views.addWidget(self.after)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addLayout(bar)
        lay.addWidget(views, 1)
        # đồng bộ cuộn và phóng
        for a, b in ((self.before, self.after), (self.after, self.before)):
            a.horizontalScrollBar().valueChanged.connect(b.horizontalScrollBar().setValue)
            a.verticalScrollBar().valueChanged.connect(b.verticalScrollBar().setValue)
            a.zoomed.connect(self.zoom)
        self.size_out = None

    def show_pair(self, src_path, out_path):
        src = QImage(str(src_path))
        out = QImage(str(out_path))
        if src.isNull() or out.isNull():
            self.info.setText("Không mở được ảnh để xem trước.")
            return
        size = (out.width(), out.height())
        self.size_out = size
        self.before.set_image(src.convertToFormat(QImage.Format_RGB888), size)
        self.after.set_image(out, size)
        self.info.setText(f"{Path(src_path).name}: {src.width()}×{src.height()} → {out.width()}×{out.height()}")
        self.fit()

    def clear(self):
        self.before.clear_image()
        self.after.clear_image()
        self.info.setText("Chọn một ảnh đã làm nét để xem trước / sau.")

    def fit(self):
        if not self.size_out:
            return
        w = self.size_out[0]
        vw = max(self.after.viewport().width() - 4, 50)
        s = vw / w
        for v in (self.before, self.after):
            v.resetTransform()
            v.scale(s, s)
            v.verticalScrollBar().setValue(0)

    def actual(self):
        for v in (self.before, self.after):
            v.resetTransform()

    def zoom(self, f):
        for v in (self.before, self.after):
            v.scale(f, f)


class DropList(QListWidget):
    dropped = Signal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setMinimumWidth(280)
        self.setMinimumHeight(80)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, e):
        self.dropped.emit([u.toLocalFile() for u in e.mimeData().urls()])

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.count() == 0:
            p = QPainter(self.viewport())
            p.setPen(QColor("#888"))
            p.drawText(self.viewport().rect(), Qt.AlignCenter,
                       "Kéo-thả ảnh hoặc thư mục vào đây\n\nhoặc bấm \"Thêm ảnh\" / \"Thêm thư mục\"")


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Làm Nét — làm nét & phóng to ảnh")
        self.resize(1200, 760)
        self.out_dir = ROOT / "outputs"
        self.items = []          # mỗi phần tử: dict(path, out, status)
        self.worker = None

        # --- cột trái: danh sách + nút
        self.list = DropList()
        self.list.dropped.connect(self.add_paths)
        self.list.currentRowChanged.connect(self.on_select)
        b_add = QPushButton("Thêm ảnh")
        b_dir = QPushButton("Thêm thư mục")
        b_clr = QPushButton("Xoá danh sách")
        b_add.clicked.connect(self.pick_files)
        b_dir.clicked.connect(self.pick_dir)
        b_clr.clicked.connect(self.clear_list)
        row_btn = QHBoxLayout()
        for b in (b_add, b_dir, b_clr):
            row_btn.addWidget(b)

        self.cb_kieu = QComboBox()
        for label, _ in KIEU:
            self.cb_kieu.addItem(label)
        self.cb_scale = QComboBox()
        self.cb_scale.addItems(["2× (đăng web)", "4× (phóng lớn)"])
        opts = QHBoxLayout()
        opts.addWidget(QLabel("Kiểu ảnh:"))
        opts.addWidget(self.cb_kieu, 1)
        opts.addWidget(QLabel("Phóng:"))
        opts.addWidget(self.cb_scale)

        self.lbl_out = QLabel()
        self.lbl_out.setWordWrap(True)
        self.lbl_out.setStyleSheet("color:#aaa;")
        b_out = QPushButton("Đổi thư mục lưu…")
        b_open = QPushButton("Mở thư mục kết quả")
        b_out.clicked.connect(self.pick_out)
        b_open.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.out_dir))))
        row_out = QHBoxLayout()
        row_out.addWidget(b_out)
        row_out.addWidget(b_open)

        self.btn_run = QPushButton("▶  Làm nét")
        self.btn_run.setMinimumHeight(40)
        self.btn_run.setStyleSheet("font-size:15px; font-weight:bold;")
        self.btn_run.clicked.connect(self.run_or_stop)
        self.bar_file = QProgressBar()
        self.bar_all = QProgressBar()
        self.lbl_status = QLabel("Sẵn sàng.")
        self.lbl_status.setWordWrap(True)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.addLayout(row_btn)
        ll.addWidget(self.list, 1)
        ll.addLayout(opts)
        ll.addWidget(self.lbl_out)
        ll.addLayout(row_out)
        ll.addWidget(self.btn_run)
        ll.addWidget(QLabel("Ảnh hiện tại:"))
        ll.addWidget(self.bar_file)
        ll.addWidget(QLabel("Cả danh sách:"))
        ll.addWidget(self.bar_all)
        ll.addWidget(self.lbl_status)

        self.preview = Preview()
        split = QSplitter(Qt.Horizontal)
        split.addWidget(left)
        split.addWidget(self.preview)
        split.setStretchFactor(1, 1)
        split.setSizes([360, 840])
        self.setCentralWidget(split)
        self.update_out_label()

    # ---------- danh sách ----------
    def add_paths(self, paths):
        added = 0
        known = {it["path"] for it in self.items}
        for p in map(Path, paths):
            files = sorted(f for f in p.iterdir() if f.suffix.lower() in EXTS) if p.is_dir() else [p]
            for f in files:
                if f.suffix.lower() in EXTS and f.is_file() and str(f) not in known:
                    self.items.append({"path": str(f), "out": None, "status": "Chờ"})
                    known.add(str(f))
                    added += 1
        self.refresh_list()
        if added and self.list.currentRow() < 0:
            self.list.setCurrentRow(0)
        self.lbl_status.setText(f"Đã thêm {added} ảnh. Tổng {len(self.items)} ảnh.")

    def refresh_list(self):
        cur = self.list.currentRow()
        self.list.blockSignals(True)
        self.list.clear()
        for it in self.items:
            mark = {"Chờ": "•", "Đang làm": "⏳", "Xong": "✔", "Lỗi": "✖", "Dừng": "■"}.get(it["status"].split(" ")[0], "•")
            QListWidgetItem(f"{mark}  {Path(it['path']).name}   — {it['status']}", self.list)
        self.list.blockSignals(False)
        if 0 <= cur < self.list.count():
            self.list.setCurrentRow(cur)

    def pick_files(self):
        fs, _ = QFileDialog.getOpenFileNames(self, "Chọn ảnh", "", "Ảnh (*.png *.jpg *.jpeg *.webp *.bmp)")
        if fs:
            self.add_paths(fs)

    def pick_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Chọn thư mục ảnh")
        if d:
            self.add_paths([d])

    def pick_out(self):
        d = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu kết quả", str(self.out_dir))
        if d:
            self.out_dir = Path(d)
            self.update_out_label()

    def update_out_label(self):
        self.lbl_out.setText(f"Lưu vào: {self.out_dir}")

    def clear_list(self):
        if self.worker:
            return
        self.items.clear()
        self.refresh_list()
        self.preview.clear()
        self.lbl_status.setText("Đã xoá danh sách.")

    def on_select(self, row):
        if 0 <= row < len(self.items) and self.items[row]["out"]:
            self.preview.show_pair(self.items[row]["path"], self.items[row]["out"])

    # ---------- chạy ----------
    def run_or_stop(self):
        if self.worker:
            self.worker.stop()
            self.btn_run.setEnabled(False)
            self.lbl_status.setText("Đang dừng sau ô hiện tại…")
            return
        jobs = [(i, it["path"]) for i, it in enumerate(self.items) if it["status"] != "Xong"]
        if not jobs:
            self.lbl_status.setText("Chưa có ảnh nào cần làm. Kéo-thả ảnh vào danh sách.")
            return
        kieu = KIEU[self.cb_kieu.currentIndex()][1]
        scale = 2 if self.cb_scale.currentIndex() == 0 else 4
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.total, self.done = len(jobs), 0
        self.bar_all.setRange(0, self.total)
        self.bar_all.setValue(0)
        self.t_start = time.perf_counter()
        self.worker = Worker(jobs, kieu, scale, self.out_dir)
        self.worker.file_started.connect(self.on_started)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_done.connect(self.on_done)
        self.worker.file_failed.connect(self.on_failed)
        self.worker.finished_all.connect(self.on_finished)
        self.set_busy(True)
        self.worker.start()

    def set_busy(self, busy):
        self.btn_run.setText("■  Dừng" if busy else "▶  Làm nét")
        self.btn_run.setEnabled(True)
        for w in (self.cb_kieu, self.cb_scale):
            w.setEnabled(not busy)

    def on_started(self, idx):
        self.items[idx]["status"] = "Đang làm"
        self.refresh_list()
        self.bar_file.setValue(0)
        self.lbl_status.setText(f"Đang làm nét: {Path(self.items[idx]['path']).name}")

    def on_progress(self, idx, i, n):
        self.bar_file.setRange(0, n)
        self.bar_file.setValue(i)

    def on_done(self, idx, out, dt):
        it = self.items[idx]
        it["out"], it["status"] = out, f"Xong ({dt:.0f} s)"
        self.done += 1
        self.bar_all.setValue(self.done)
        self.refresh_list()
        self.list.setCurrentRow(idx)
        self.preview.show_pair(it["path"], out)

    def on_failed(self, idx, msg):
        self.items[idx]["status"] = "Lỗi"
        self.done += 1
        self.bar_all.setValue(self.done)
        self.refresh_list()
        self.lbl_status.setText(f"Lỗi với {Path(self.items[idx]['path']).name}: {msg}")

    def on_finished(self, stopped):
        for it in self.items:
            if it["status"] == "Đang làm":
                it["status"] = "Dừng"
        self.refresh_list()
        self.worker = None
        self.set_busy(False)
        mins = (time.perf_counter() - self.t_start) / 60
        self.lbl_status.setText(("Đã dừng. " if stopped else "Hoàn tất. ") +
                                f"{self.done}/{self.total} ảnh trong {mins:.1f} phút. Kết quả ở: {self.out_dir}")

    def closeEvent(self, e):
        if self.worker:
            if QMessageBox.question(self, "Đang làm nét", "Đang xử lý ảnh. Dừng và thoát?") != QMessageBox.Yes:
                e.ignore()
                return
            self.worker.stop()
            self.worker.wait(30000)
        e.accept()


def main():
    def hook(t, v, tb):
        msg = "".join(traceback.format_exception(t, v, tb))
        log("CRASH\n" + msg)
        sys.__stderr__.write(msg)
    sys.excepthook = hook
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Main()
    scr = app.primaryScreen().availableGeometry()
    if scr.height() < 800 or scr.width() < 1250:
        w.showMaximized()        # màn hình nhỏ: mở toàn màn hình để không bị taskbar che
    else:
        w.show()
    if len(sys.argv) > 1:
        w.add_paths(sys.argv[1:])
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
