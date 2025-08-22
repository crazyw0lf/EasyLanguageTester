from functools import partial
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QSize


class LevelPage(QWidget):
    level_selected = pyqtSignal(str)
    back_requested = pyqtSignal()
    def __init__(self, levels = None):
        super().__init__()
        if levels is None:
            levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        top = QHBoxLayout()
        btn_back = QPushButton()
        btn_back.setFixedSize(40,40)
        btn_back.setIcon(QIcon("resources/back icon.png"))
        btn_back.setIconSize(QSize(30,30))
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

        title = QLabel("Select Level")
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

        for i, name in enumerate(levels):
            b = QPushButton(name)
            b.setStyleSheet(f"""text-align: center;
                            font-size: 20px;
                            background-color: {colors[i % len(colors)]};
                            color: white;
                            border: none;
                            border-radius: 8px;""")
            b.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    text-align: center;
                    color: white;

                    border: 2px solid #333;   /* constant width → no jump */
                    border-radius: 6px;
                    background-color: {colors[i % len(colors)]};
                }}
                QPushButton:hover {{
                    border-color: #b0b0b0;                 /* visual cue only */
                    background-color: {colors[i % len(colors)].replace("0.5", "1")};
                }}
                QPushButton:pressed {{
                    border-color: #888;
                    background-color: {colors[i % len(colors)].replace("0.5", "1")};
                }}
            """)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(56)

            sp = b.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            sp.setVerticalPolicy(QSizePolicy.Expanding)
            b.setSizePolicy(sp)

            b.clicked.connect(partial(self.level_selected.emit, name))
            g.addWidget(b, i // 3, i % 3)

        for c in range(3):
            g.setColumnStretch(c,1)
        for r in range(2):
            g.setRowStretch(r,1)