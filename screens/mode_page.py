from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

class ModePage(QWidget):
    mode_selected = pyqtSignal(str)
    def __init__(self, modes = None):
        super().__init__()
        if modes is None:
            modes = ['Words and Grammar', 'Reading', 'Listening']

            v = QVBoxLayout(self)
            v.setContentsMargins(24,24,24,24)
            v.setSpacing(16)

            title = QLabel("Select Test Mode")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 28px; font-weight: 600;")
            v.addWidget(title)

            g = QGridLayout()
            g.setSpacing(24)
            v.addLayout(g,1)

            for i, mode in enumerate(modes):
                b = QPushButton(mode)
                b.setMinimumHeight(56)

                sp = b.sizePolicy()
                sp.setHorizontalPolicy(QSizePolicy.Expanding)
                sp.setVerticalPolicy(QSizePolicy.Expanding)
                b.setSizePolicy(sp)

                url = "resources/" + f"{mode.lower()} icon.png"
                b.setStyleSheet(f"""
                    QPushButton {{
                        font-size: 20px;
                        font-weight: bold;
                        color: white;
                        text-align: center top;

                        /* keep some gap above and reserve space below for the image */
                        padding-top: 100px;
                        padding-bottom: 100px;   /* <- tune this to move the image lower/higher */

                        border: 2px solid #333;
                        border-radius: 6px;

                        background-image: url("{url}");
                        background-repeat: no-repeat;
                        background-position: center bottom;  /* image sits a bit lower */
                        background-origin: content;
                        background-clip: content;
                    }}
                """)

                b.clicked.connect(partial(self.mode_selected.emit, mode))
                g.addWidget(b,0,i % 3)

            for c in range(3):
                g.setColumnStretch(c,1)
            g.setRowStretch(0,1)