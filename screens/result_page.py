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
                    border-color: #b0b0b0;                 /* visual cue only */
                    background-color: rgba(255,255,255,0.2);
                }
                """

        self.tps = 150
        self.current_score = 0
        self.target_score = evaluate_score

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / self.tps)

        v = QVBoxLayout(self)
        # v.setContentsMargins(24,24,24,24)
        # v.setSpacing(16)

        title = QLabel(self.labels[min(self.target_score//20,4)])
        title.setAlignment(Qt.AlignHCenter)
        title.setStyleSheet("font-size: 40px; font-weight: 600;")
        v.addWidget(title,1)

        self.score = QLabel(str(self.current_score))
        self.score.setAlignment(Qt.AlignHCenter)
        self.score.setStyleSheet("font-size: 28px; font-weight: 300;")
        v.addWidget(self.score,1)

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

    def update(self):
        if self.current_score >= self.target_score:
            self.current_score = self.target_score
            self.timer.stop()
            return
        self.current_score += 1

        self.score.setText(str(self.current_score))
        self.score.setAlignment(Qt.AlignHCenter)
        self.score.adjustSize()

        self.tps -= 2
        if self.tps <= 5:
            self.tps = 5
        self.timer.setInterval(1000 / self.tps)