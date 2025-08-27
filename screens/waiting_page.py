import sys, random
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class WaitingPage(QWidget):

    def __init__(self, labels: list = None):
        super().__init__()
        self.labels = labels
        if self.labels is None:
            self.labels = []
        self.labels += ["This may take a moment",
                           "Please wait",
                           "Wait a bit",
                           "Loading",]

        v = QVBoxLayout(self)
        v.setAlignment(Qt.AlignCenter)
        v.setContentsMargins(0,0,0,0)
        v.setSpacing(12)

        spinner = VariableWedgeSpinner(
            size=120,
            thickness=12,
            bg_color=QColor("#d1d5db"),  # light grey
            light_color=QColor("#ffffff"),  # white
            rps=0.9,
            change_interval_ms=1000
        )

        self.text = random.choice(self.labels)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(self.text)
        self.label.setStyleSheet("font-size: 20px; font-weight: 300;")

        v.addWidget(spinner,0, Qt.AlignHCenter)
        v.addWidget(self.label,0, Qt.AlignHCenter)

        self.timer = QTimer(self)
        self.timer.setInterval(random.randint(200, 1000))
        self.timer.timeout.connect(self.add_dot)
        self.timer.start()

    def add_dot(self):
        if "..." in self.text:
            lbls = self.labels.copy()
            lbls.remove(self.text[:-3])  # remove current text without dots
            self.text = random.choice(lbls)
            self.label.setText(self.text)
        else:
            self.text += "."
            self.label.setText(str(self.text))
        self.timer.setInterval(random.randint(200, 1000))

class VariableWedgeSpinner(QWidget):
    """
    A rotating ring with a light sector that randomly changes size
    between 90° and 180° every 5 seconds.

    Parameters
    ----------
    size : int            -> diameter of the widget
    thickness : float     -> ring thickness
    bg_color : QColor     -> color of the non-light part (e.g., light grey)
    light_color : QColor  -> color of the light sector (e.g., white)
    rps : float           -> rotations per second for continuous spin
    change_interval_ms : int -> how often to choose a new sector size
    """
    def __init__(
        self,
        size=88,
        thickness=10,
        bg_color=QColor("#d1d5db"),      # light grey
        light_color=QColor("#ffffff"),   # white
        rps=0.8,
        change_interval_ms=5000,
        parent=None,
    ):
        super().__init__(parent)
        self._size = int(size)
        self._thickness = float(thickness)
        self._bg_color = QColor(bg_color)
        self._light_color = QColor(light_color)
        self._rps = float(rps)

        # rotation + timekeeping
        self._angle_deg = 0.0
        self._elapsed = QElapsedTimer()

        # sector span (in degrees)
        self._span_deg = 180.0       # start at half circle
        self._target_span_deg = 180.0

        # timers
        self._anim_timer = QTimer(self)
        self._anim_timer.setTimerType(Qt.PreciseTimer)
        self._anim_timer.setInterval(16)  # ~60 FPS
        self._anim_timer.timeout.connect(self._on_anim)

        self._change_timer = QTimer(self)
        self._change_timer.setInterval(change_interval_ms)
        self._change_timer.timeout.connect(self._pick_new_span)

        # widget setup
        self.setMinimumSize(self._size, self._size)
        self.setMaximumSize(self._size, self._size)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # start animating
        self._elapsed.start()
        self._anim_timer.start()
        self._change_timer.start()

    # -------- Behavior --------
    def _pick_new_span(self):
        # pick a random span between 90° and 180°
        self._target_span_deg = random.uniform(90.0, 180.0)

    def _on_anim(self):
        ms = self._elapsed.restart()

        # rotate continuously
        self._angle_deg = (self._angle_deg + 360.0 * self._rps * (ms / 1000.0)) % 360.0

        # ease current span toward the target for a smooth change
        # simple critically-damped-ish smoothing:
        k = 7.0   # higher -> faster settling
        alpha = 1.0 - pow(2.718281828, -k * (ms / 1000.0))
        self._span_deg += (self._target_span_deg - self._span_deg) * alpha

        self.update()

    # -------- Painting --------
    def paintEvent(self, _event):
        size = min(self.width(), self.height())
        radius = size / 2.0 - self._thickness / 2.0

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.translate(self.rect().center())
        p.rotate(self._angle_deg)

        # base ring (full 360°) in bg_color
        base_pen = QPen(self._bg_color)
        base_pen.setWidthF(self._thickness)
        base_pen.setCapStyle(Qt.RoundCap)
        p.setPen(base_pen)
        p.setBrush(Qt.NoBrush)

        rect = (-radius, -radius, radius * 2, radius * 2)
        p.drawArc(*rect, 0, 360 * 16)

        # light sector in white
        light_pen = QPen(self._light_color)
        light_pen.setWidthF(self._thickness)
        light_pen.setCapStyle(Qt.RoundCap)
        p.setPen(light_pen)

        # draw an arc starting at 0°, spanning self._span_deg
        # (Qt angles are in 1/16th of a degree, counterclockwise)
        start_angle_16 = 0 * 16
        span_angle_16 = int(self._span_deg * 16)
        p.drawArc(*rect, start_angle_16, span_angle_16)

        p.end()

    # -------- Optional setters --------
    def setColors(self, bg_color: QColor, light_color: QColor):
        self._bg_color = QColor(bg_color)
        self._light_color = QColor(light_color)
        self.update()

    def setThickness(self, thickness: float):
        self._thickness = float(thickness)
        self.update()

    def setSpeed(self, rotations_per_sec: float):
        self._rps = float(rotations_per_sec)

    def setChangeInterval(self, ms: int):
        self._change_timer.setInterval(int(ms))
