from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray
import os

class LanguagePage(QWidget):
    language_selected = pyqtSignal(str)
    def __init__(self, languages = None):
        super().__init__()
        if languages is None:
            languages = ["Spanish", "French", "German", "Chinese", "Japanese", "Italian"]

        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        title = QLabel("Select Language")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(title)

        g = QGridLayout()
        g.setSpacing(24)
        v.addLayout(g,1)

        for i, name in enumerate(languages):
            b = QPushButton(name)
            b.setMinimumHeight(56)

            sp = b.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            sp.setVerticalPolicy(QSizePolicy.Expanding)
            b.setSizePolicy(sp)

            url = "resources/" + f"{name.lower()}.png"
            b.setStyleSheet(f"""
                QPushButton {{
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                    text-align: center top;

                    /* keep some gap above and reserve space below for the image */
                    padding-top: 20px;
                    padding-bottom: 36px;   /* <- tune this to move the image lower/higher */

                    border: 2px solid #333;
                    border-radius: 6px;

                    background-image: url("{url}");
                    background-repeat: no-repeat;
                    background-position: center bottom;  /* image sits a bit lower */
                    background-origin: content;
                    background-clip: content;
                }}
            """)

            b.clicked.connect(partial(self.language_selected.emit, name))
            g.addWidget(b, i // 3, i % 3)

        for c in range(3):
            g.setColumnStretch(c,1)
        for r in range(2):
            g.setRowStretch(r,1)

    def icon_from_svg(self, svg_text: str, w: int = 150, h: int = 100) -> QPixmap:
        render = QSvgRenderer(QByteArray(svg_text.encode('utf-8')))
        pm = QPixmap(w,h)
        pm.fill(Qt.transparent)
        painter = QPainter(pm)
        render.render(painter)
        painter.end()
        return pm