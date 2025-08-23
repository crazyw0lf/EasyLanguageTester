from functools import partial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                    QPushButton, QGridLayout, QSizePolicy,
                    QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt, QSize

class BtnChoicePage(QWidget):
    info_selected = pyqtSignal(str)
    back_requested = pyqtSignal()
    def __init__(self, btn_choices = None,
                 title_text = None,back_btn = False,
                 style = None):
        super().__init__()
        if btn_choices is None:
            raise Exception('No titles provided for buttons')
        if style is None:
            raise Exception('No style provided for buttons')

        d = len(btn_choices)
        col = 3
        row = d // 3 + (1 if d % 3 != 0 else 0)

        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        if back_btn:
            self.create_back_btn(v)

        title = QLabel(f"Select {title_text}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(title)

        g = QGridLayout()
        g.setSpacing(24)
        v.addLayout(g,1)

        colors = [
            "rgba(0, 100, 0, 0.5)",  # dark green
            "rgba(0, 139, 139, 0.5)",  # dark cyan / sea
            "rgba(0, 0, 139, 0.5)",  # dark blue
            "rgba(155, 135, 12, 0.5)",  # dark yellow (olive/goldenrod)
            "rgba(255, 140, 0, 0.5)",  # dark orange
            "rgba(139, 0, 0, 0.5)",  # dark red
        ]

        for i, btn_name in enumerate(btn_choices):
            b = QPushButton(btn_name)
            b.setMinimumHeight(56)
            b.setCursor(Qt.PointingHandCursor)

            sp = b.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            sp.setVerticalPolicy(QSizePolicy.Expanding)
            b.setSizePolicy(sp)

            url = "resources/" + f"{btn_name.lower()}.png"
            if "image" in style:
                b.setStyleSheet(style.format(url))
            else:
                b.setStyleSheet(style.format(
                    colors[i % len(colors)],
                    colors[i % len(colors)].replace("0.5", "1"),
                    colors[i % len(colors)].replace("0.5", "1")))

            b.clicked.connect(partial(self.info_selected.emit, btn_name))
            g.addWidget(b, i // col, i % col)

        for c in range(col):
            g.setColumnStretch(c,1)
        for r in range(row):
            g.setRowStretch(r,1)

    def create_back_btn(self,v):
        top = QHBoxLayout()
        btn_back = QPushButton()
        btn_back.setFixedSize(40, 40)
        btn_back.setIcon(QIcon("resources/back icon.png"))
        btn_back.setIconSize(QSize(30, 30))
        btn_back.setToolTip("Back")
        btn_back.setCursor(Qt.PointingHandCursor)
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