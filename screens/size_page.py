from functools import partial
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QSize

class SizePage(QWidget):
    size_selected = pyqtSignal(int)
    back_requested = pyqtSignal()
    def __init__(self, sizes = None):
        super().__init__()
        if sizes is None:
            sizes = [10,20,30]

        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        top = QHBoxLayout()
        btn_back = QPushButton()
        btn_back.setFixedSize(40,40)
        btn_back.setIcon(QIcon("resources/back icon.png"))
        btn_back.setIconSize(QSize(30,30))
        btn_back.setToolTip("Back")
        btn_back.setCursor(QCursor(Qt.PointingHandCursor))
        btn_back.clicked.connect(self.back_requested.emit)

        btn_back.setStyleSheet("""
            QPushButton {
                border: 1px solid #444;
                border-radius: 8px;
                background-color: rgba(255,255,255,0.04);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.08);
            }
            QPushButton:pressed {
                background-color: rgba(255,255,255,0.12);
            }
        """)

        top.addWidget(btn_back)
        top.addStretch(1)
        v.addLayout(top)

        title = QLabel("Select Test Size")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(title)

        g = QGridLayout()
        g.setSpacing(24)
        v.addLayout(g,1)

        for i, name in enumerate(sizes):
            b = QPushButton(f"{name} Questions")
            b.setMinimumHeight(56)

            sp = b.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            sp.setVerticalPolicy(QSizePolicy.Expanding)
            b.setSizePolicy(sp)

            url = "resources/" + f"{name} questions mode.png"
            b.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center top;
                    color: white;

                    /* text centered horizontally; vertical position via padding */
                    padding-top: 20px;      /* space above text */
                    padding-bottom: 36px;   /* reserves space below for the image */

                    border: 2px solid #333;   /* constant width → no jump */
                    border-radius: 6px;
                    background-color: rgba(255,255,255,0.04);

                    background-image: url("{url}");
                    background-repeat: no-repeat;
                    background-origin: content;
                    background-position: center bottom;  /* image sits lower */
                }}
                QPushButton:hover {{
                    border-color: #b0b0b0;                 /* visual cue only */
                    background-color: rgba(255,255,255,0.08);
                }}
                QPushButton:pressed {{
                    border-color: #888;
                    background-color: rgba(255,255,255,0.12);
                }}
            """)
            b.setCursor(QCursor(Qt.PointingHandCursor))
            b.clicked.connect(partial(self.size_selected.emit, name))
            g.addWidget(b, 0, i % 3)

        for c in range(3):
            g.setColumnStretch(c,1)
        g.setRowStretch(0,1)