from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt

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
            b.setCursor(Qt.PointingHandCursor)

            b.clicked.connect(partial(self.language_selected.emit, name))
            g.addWidget(b, i // 3, i % 3)

        for c in range(3):
            g.setColumnStretch(c,1)
        for r in range(2):
            g.setRowStretch(r,1)