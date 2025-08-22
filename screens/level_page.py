from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt

class LevelPage(QWidget):
    level_selected = pyqtSignal(str)
    def __init__(self, levels = None):
        super().__init__()
        if levels is None:
            levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        title = QLabel("Select Level")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(title)

        g = QGridLayout()
        g.setSpacing(24)
        v.addLayout(g,1)

        colors = [
            "#006400",  # dark green
            "#008B8B",  # dark cyan / sea
            "#00008B",  # dark blue
            "#9B870C",  # dark yellow (olive/goldenrod tone)
            "#FF8C00",  # dark orange
            "#8B0000",  # dark red
        ]

        for i, name in enumerate(levels):
            b = QPushButton(name)
            b.setStyleSheet("text-align: center;"
                            "font-size: 20px;"
                            "background-color: {}; color: white; border: none; border-radius: 8px;".format(colors[i % len(colors)]))
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