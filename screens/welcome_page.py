from functools import partial
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, Qt
from styles.btn_styles import confirm_btn_style

class WelcomePage(QWidget):
    topic = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

        self.label = QLabel("Hello, I am QuizBot!\nWhat topic do you want to practice today?")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 40px; font-weight: 500;")
        self.layout.addWidget(self.label)

        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Type your answer here...")
        self.input_area.setMinimumHeight(100)
        self.input_area.setFont(QFont("Arial", 20))
        sp = self.input_area.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        self.input_area.setSizePolicy(sp)
        self.input_area.textChanged.connect(lambda: self.con_btn.setEnabled(True))

        self.layout.addWidget(self.input_area)
        self.layout.addWidget(self.input_area, 1)

        self.con_btn = QPushButton("Confirm")
        self.con_btn.setFixedSize(200, 56)
        self.con_btn.setCursor(Qt.PointingHandCursor)
        self.con_btn.setEnabled(False)
        self.con_btn.clicked.connect(self._confirm_ans)
        self.con_btn.setStyleSheet(confirm_btn_style)
        self.layout.addWidget(self.con_btn, alignment=Qt.AlignHCenter | Qt.AlignBottom)
    
    def _confirm_ans(self):
        self.topic.emit(self.input_area.text())