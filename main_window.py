from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QSizePolicy, QLabel, QStackedWidget,
                             QGridLayout, QMessageBox, QFileDialog,
                             QPushButton)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from screens.btn_choice_page import BtnChoicePage
from styles.btn_styles import lang_page_style, level_page_style, size_page_style, mode_page_style
from screens.result_page import ResultPage
from screens.waiting_page import WaitingPage
from screens.test_question_page import QuestionPage, QuestionWaitPage, Qtyp
from screens.welcome_page import WelcomePage
from core import Core
from functools import partial
import json

class StartPage(QWidget):
    create_new = pyqtSignal()
    import_test = pyqtSignal()

    def __init__(self):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(24,24,24,24)
        v.setSpacing(16)

        # Title
        title = QLabel("Welcome to Language Test Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        v.addWidget(title)

        # Grid for buttons
        g = QGridLayout()
        g.setSpacing(24)
        v.addLayout(g,1)

        # Choices
        choices = [("Create New Test", self.create_new), ("Import from JSON", self.import_test)]
        colors = [
            "rgba(200, 0 , 0, 0.5)",
            "rgba(0, 0, 139, 0.5)",
        ]

        for i,(label,signal) in enumerate(choices):
            b = QPushButton(label)
            b.setMinimumHeight(80)
            b.setCursor(Qt.PointingHandCursor)

            sp = b.sizePolicy()
            sp.setHorizontalPolicy(QSizePolicy.Expanding)
            sp.setVerticalPolicy(QSizePolicy.Expanding)
            b.setSizePolicy(sp)

            # Apply consistent style (same as BtnChoicePage)
            b.setStyleSheet(level_page_style.format(
                colors[i % len(colors)],
                colors[i % len(colors)].replace("0.5","1"),
            ))

            b.clicked.connect(signal.emit)
            g.addWidget(b, 0, i)

        for c in range(2):
            g.setColumnStretch(c,1)
        g.setRowStretch(0,1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("resources/icon.png"))
        self.setWindowTitle("Language Test Generator")
        self.resize(1000,700)

        self.language = None
        self.level = None
        self.size = None

        central = QWidget(self); self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.startPage = StartPage()
        self.welcomePage = WelcomePage()
        self.langPage = BtnChoicePage(["Spanish", "French", "German", "Chinese", "Japanese", "Italian"],
                                      "Language",style = lang_page_style)
        self.levelPage = BtnChoicePage(["A1", "A2", "B1", "B2", "C1", "C2"],
                                       "Level", back_btn=True, style = level_page_style)
        self.sizePage = BtnChoicePage(["10","20","30"], "Test Size", back_btn=True,
                                      style = size_page_style)
        self.waitPage = WaitingPage()

        self.stack.addWidget(self.startPage)
        self.stack.addWidget(self.welcomePage)
        self.stack.addWidget(self.langPage)
        self.stack.addWidget(self.levelPage)
        self.stack.addWidget(self.sizePage)
        self.stack.addWidget(self.waitPage)

        self.stack.setCurrentWidget(self.startPage)

        self.startPage.create_new.connect(lambda: self.stack.setCurrentWidget(self.welcomePage))
        self.startPage.import_test.connect(self.import_test_dialog)
        self.welcomePage.topic.connect(self._on_topic)
        self.langPage.info_selected.connect(self._on_language)
        self.levelPage.info_selected.connect(self._on_level)
        self.sizePage.info_selected.connect(self._on_size)

        self.levelPage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.langPage))
        self.sizePage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.levelPage))

    def create_question(self):
        self.prequestionPage = QuestionWaitPage(self.test[str(self.cur_index)]["question"],
                                         int(self.type_stats[self.test[str(self.cur_index)]['type']]['pretime']))
        self.questionPage = QuestionPage(self.test[str(self.cur_index)]["type"],
                                         self.test[str(self.cur_index)]["question"],
                                         self.test[str(self.cur_index)]["answers"],
                                         int(self.type_stats[self.test[str(self.cur_index)]['type']]['time']))
        self.stack.addWidget(self.prequestionPage)
        self.stack.addWidget(self.questionPage)
        self.stack.setCurrentWidget(self.prequestionPage)
        self.prequestionPage.ready.connect(self.start_question)
        self.questionPage.answer_selected.connect(self._answer_selected)

    def start_question(self):
        self.stack.setCurrentWidget(self.questionPage)
        self.questionPage.start_timer()

    def _run_again(self):
        self.cur_index = 1
        self.create_question()

    def create_result(self,score):
        score = int((self.score + score) / self.max_score * 100)
        score = min(score, 100)
        self.resPage = ResultPage(score)

        self.resPage.run_again.connect(self._run_again)
        self.resPage.start_new.connect(lambda: self.stack.setCurrentWidget(self.welcomePage))
        self.resPage.save_test.connect(self.save_test_dialog)

        self.stack.addWidget(self.resPage)
        self.stack.setCurrentWidget(self.resPage)

    def import_test_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Test File",
            "test.json",
            "JSON Files (*.json)",
            options=options
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    test = json.load(file)
                    self._on_test_created(test)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def save_test_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Test File As",
            "test.json",
            "JSON Files (*.json);;All Files(*)",
            options=options
        )

        if file_path:
            with open(file_path, 'w') as outfile:
                outfile.write(json.dumps(self.test, indent=4, ensure_ascii=False))

    def _answer_selected(self, ans):
        print("Selected answer:", ans)
        print("Right answer:", self.test[str(self.cur_index)]["right_answer"])
        self.ans_sheet = {}
        if self.test[str(self.cur_index)]['type'] == Qtyp.hard:
            self.ans_sheet[str(self.cur_index)] = {"user_answer": ans,"right_answer": self.test[str(self.cur_index)]["right_answer"]}
        elif ans == self.test[str(self.cur_index)]["right_answer"]:
            self.score += int(self.type_stats[self.test[str(self.cur_index)]['type']]['score'])
        if self.cur_index < len(self.test):
            self.cur_index += 1
            self.create_question()
        else:
            self.stack.setCurrentWidget(self.waitPage)
            self.evaluate_test_bg()

    def _on_topic(self, topic):
        self.topic = topic
        self.stack.setCurrentWidget(self.langPage)
    def _on_language(self, lang):
        self.language = lang
        self.stack.setCurrentWidget(self.levelPage)
    def _on_level(self, level):
        self.level = level
        self.stack.setCurrentWidget(self.sizePage)
    def _on_size(self, size):
        self.size = size
        self.stack.setCurrentWidget(self.waitPage)
        self.create_test_bg()

    def evaluate_test_bg(self):

        self._thread = QThread()
        self._worker = Core(self)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(partial(self._worker.evaluate, self.ans_sheet))
        self._worker.evaluated.connect(self.create_result)
        self._worker.errored.connect(self._on_test_error)

        self._worker.evaluated.connect(self._thread.quit)
        self._worker.evaluated.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.errored.connect(self._thread.quit)
        self._worker.errored.connect(self._worker.deleteLater)
        self._thread.start()

    def create_test_bg(self):

        self._thread = QThread()
        self._worker = Core(self)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_test_created)
        self._worker.errored.connect(self._on_test_error)

        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.errored.connect(self._thread.quit)
        self._worker.errored.connect(self._worker.deleteLater)
        self._thread.start()

    def _on_test_created(self,test):
        self.test = test

        self.cur_index = 1
        self.type_stats = {Qtyp.light : {"score" : "3", "time": "10", "pretime": "3"},
                           Qtyp.medium : {"score" : "6", "time": "30", "pretime": "3"},
                           Qtyp.hard : {"score" : "10", "time": "60", "pretime": "5"}}
        self.max_score = 0
        self.score = 0
        for k in self.test:
            self.max_score += int(self.type_stats[self.test[k]['type']]['score'])

        self.create_question()

    def _on_test_error(self, err):
        QMessageBox.critical(self, "Error:", err)
        self.stack.setCurrentWidget(self.welcomePage)