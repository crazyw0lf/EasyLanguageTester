from functools import partial

from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QGridLayout, QSizePolicy,
                             QProgressBar, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from enum import IntEnum
from styles.btn_styles import confirm_btn_style, question_btn_style

class Qtyp(IntEnum):
    light = 0
    medium = 1
    hard = 2


class QuestionPage(QWidget):
    answer_selected = pyqtSignal(str)

    def __init__(self, typ: Qtyp, question: str, answers: list = None, sec: int = 10):
        super().__init__()
        self.typ = typ
        self.question = question
        self.answers = answers
        self.selected_answer = ""
        self.selected_btn = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

        self.qlabel = QLabel(self.question)
        self.qlabel.setWordWrap(True)
        self.qlabel.setAlignment(Qt.AlignCenter)
        self.qlabel.setStyleSheet("font-size: 40px; font-weight: 500;")
        self.layout.addWidget(self.qlabel)
        self.layout.addStretch(1)

        self.setup_question()
        self.layout.addStretch(1)

        self.con_btn = QPushButton("Confirm")
        self.con_btn.setFixedSize(200, 56)
        self.con_btn.setCursor(Qt.PointingHandCursor)
        self.con_btn.setEnabled(False)
        self.con_btn.clicked.connect(self._confirm_ans)
        self.con_btn.setStyleSheet(confirm_btn_style)
        self.layout.addWidget(self.con_btn, alignment=Qt.AlignHCenter | Qt.AlignBottom)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
                    QProgressBar {
                        background-color: #949494;
                        border: none;
                        border-radius: 10px;
                    }
                    QProgressBar::chunk {
                        background-color: #ffffff;
                        border-radius: 10px;
                    }
                """)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.timer = QTimer()
        self.timer.setInterval(sec * 10)
        self.timer.timeout.connect(self.update_progress)

    def start_timer(self):
        self.timer.start()

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()
            self.answer_selected.emit("")

    def wrap_text(self, text, font, max_width):
        fm = QFontMetrics(font)
        words = text.split()
        lines, line = [], ""

        for w in words:
            test = w if line == "" else line + " " + w
            if fm.horizontalAdvance(test) <= max_width:
                line = test
            else:
                if line:  # push finished line
                    lines.append(line)
                line = w
        if line:
            lines.append(line)

        return "\n".join(lines)

    def setup_question(self):
        if self.typ != Qtyp.hard:
            layout = QGridLayout()
            layout.setSpacing(50)
            btn_labels = self.answers

            for i,btn_label in enumerate(btn_labels):
                btn = QPushButton()
                btn.setCheckable(True)
                btn.setChecked(False)
                btn.setMinimumSize(150,150)
                btn.setMaximumSize(500,500)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(question_btn_style)

                wraped = self.wrap_text(btn_label, btn.font(), 200)
                btn.setText(wraped)

                sp = btn.sizePolicy()
                sp.setHorizontalPolicy(QSizePolicy.Expanding)
                sp.setVerticalPolicy(QSizePolicy.Expanding)
                btn.setSizePolicy(sp)

                btn.clicked.connect(partial(self._selected_ans_btn, btn))
                layout.addWidget(btn,i//2,i%2)
            self.layout.addLayout(layout,1)

        if self.typ == Qtyp.hard:
            input_area = QLineEdit()
            input_area.setPlaceholderText("Type your answer here...")
            input_area.setMinimumHeight(100)
            input_area.setFont(QFont("Arial", 20))
            sp = input_area.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            input_area.setSizePolicy(sp)
            input_area.textChanged.connect(partial(self._selected_ans_text, input_area))
            self.layout.addWidget(input_area,1)

    def _selected_ans_btn(self, ans):
        self.selected_answer = ans.text().replace('\n','')
        if self.selected_btn:
            self.selected_btn.setChecked(False)
        self.selected_btn = ans
        ans.setChecked(True)
        self.con_btn.setEnabled(True)

    def _selected_ans_text(self,ans):
        self.selected_answer = ans.text()
        self.con_btn.setEnabled(True)

    def _confirm_ans(self):
        self.answer_selected.emit(self.selected_answer)
        self.timer.stop()


class QuestionWaitPage(QWidget):
    ready = pyqtSignal()
    def __init__(self, text: str, sec: int = 5):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 40px; font-weight: 500;")
        self.layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #949494;
                border: none;
                border-radius: 10px;
            }
            QProgressBar::chunk {
                background-color: #ffffff;
                border-radius: 10px;
            }
        """)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar)

        self.timer = QTimer()
        self.timer.setInterval(sec * 10)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start()

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()
            self.ready.emit()