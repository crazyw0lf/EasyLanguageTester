from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class WorkPage(QWidget):
    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        label = QLabel("Work in Progress...")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(label)