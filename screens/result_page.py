from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QGridLayout, QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer

class ResultPage(QWidget):
    run_again = pyqtSignal()
    save_test = pyqtSignal()
    start_new = pyqtSignal()

    def __init__(self, evaluate_score: int):
        super().__init__()
        self.labels = ['This test was too hard for you!', 'You should aspire more!', 'Try Better!', 'Good!', 'Excellent!']
        self.style = """                    
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center;
                    color: white;

                    border: 2px solid #333;   /* constant width → no jump */
                    border-radius: 6px;
                    background-color: rgba(255,255,255,0.04);
                }
                QPushButton:hover {
                    border-color: #b0b0b0;
                    background-color: rgba(255,255,255,0.2);
                }
                """

        # --- score animation state ---
        self.tps = 150
        self.current_score = 0
        self.target_score = evaluate_score

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / self.tps)

        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        center_block = QVBoxLayout()
        center_block.setSpacing(12)
        center_block.setAlignment(Qt.AlignCenter)

        title = QLabel(self.labels[min(self.target_score//20,4)])
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("font-size: 40px; font-weight: 600;")
        v.addWidget(title,1)

        # --- STARS ROW (above score) ---
        self.star_size = QSize(56, 56)  # tweak as desired
        self.star_on_px = QPixmap("resources/star.png")
        self.star_off_px = QPixmap("resources/starplace.png")

        stars_row = QHBoxLayout()
        stars_row.setSpacing(6)
        stars_row.setAlignment(Qt.AlignHCenter)
        self.star_labels = []
        for _ in range(3):
            lbl = QLabel()
            lbl.setFixedSize(self.star_size)
            lbl.setScaledContents(True)  # keep it simple; images are square
            self.star_labels.append(lbl)
            stars_row.addWidget(lbl,1)
        center_block.addLayout(stars_row, 1)

        # initialize with 0 stars
        self._set_stars(0)

        # --- SCORE LABEL ---
        self.score = QLabel(str(self.current_score))
        self.score.setAlignment(Qt.AlignCenter)
        self.score.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.score.setStyleSheet("font-size: 28px; font-weight: 300;")
        center_block.addWidget(self.score,1)

        v.addLayout(center_block,4)

        # --- BUTTONS ---
        h = QHBoxLayout()
        h.setSpacing(8)

        run_btn = QPushButton("Run Again")
        save_btn = QPushButton("Save Test")
        new_btn = QPushButton("New Test")

        for btn in (run_btn, save_btn, new_btn):
            btn.setStyleSheet(self.style)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(QSize(240, 80))
            h.addWidget(btn)

        run_btn.clicked.connect(self.run_again.emit)
        save_btn.clicked.connect(self.save_test.emit)
        new_btn.clicked.connect(self.start_new.emit)

        v.addLayout(h,1)

    # --- helper: decide how many stars for a score ---
    def _stars_for(self, s: int) -> int:
        if s >= 90:
            return 3
        if s >= 75:
            return 2
        if s >= 50:
            return 1
        return 0

    # --- helper: paint stars row ---
    def _set_stars(self, count: int):
        for i, lbl in enumerate(self.star_labels):
            px = self.star_on_px if i < count else self.star_off_px
            lbl.setPixmap(px.scaled(self.star_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update(self):
        if self.current_score >= self.target_score:
            self.current_score = self.target_score
            self.timer.stop()
        else:
            self.current_score += 1

        # update score text
        self.score.setText(str(self.current_score))

        # update stars according to the (animated) score
        self._set_stars(self._stars_for(self.current_score))

        # accelerate → then clamp
        self.tps -= 2
        if self.tps <= 5:
            self.tps = 5
        self.timer.setInterval(1000 / self.tps)
