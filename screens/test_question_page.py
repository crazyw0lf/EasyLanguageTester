from functools import partial
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QGridLayout, QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from enum import IntEnum
from styles.btn_styles import question_page_style

class Qtyp(IntEnum):
    light = 0
    medium = 1
    hard = 2


class QuestionPage(QWidget):
    answer_selected = pyqtSignal(str)

    def __init__(self, typ: Qtyp, question: str, right_answer: str, wrong_answers: list):
        super().__init__()
        self.typ = typ
        self.question = question
        self.right_answer = right_answer
        self.wrong_answers = wrong_answers
        self.selected_answer = ""

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

        self.qlabel = QLabel(self.question)
        self.qlabel.setAlignment(Qt.AlignCenter)
        self.qlabel.setStyleSheet("font-size: 24px; font-weight: 500;")
        self.layout.addWidget(self.qlabel)
        self.layout.addStretch(1)

        self.con_btn = QPushButton("Confirm")
        self.con_btn.setFixedSize(200, 56)
        self.con_btn.setCursor(Qt.PointingHandCursor)
        self.con_btn.setEnabled(False)
        self.con_btn.clicked.connect(partial(self.answer_selected.emit, self.selected_answer))
        self.con_btn.setStyleSheet(question_page_style)
        self.layout.addWidget(self.con_btn, alignment=Qt.AlignHCenter | Qt.AlignBottom)