from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QStackedWidget, QLineEdit)
from screens.btn_choice_page import BtnChoicePage
from styles.btn_styles import lang_page_style, level_page_style, size_page_style, mode_page_style
from screens.result_page import ResultPage
from screens.waiting_page import WaitingPage
from screens.test_question_page import QuestionPage, QuestionWaitPage, Qtyp
from screens.welcome_page import WelcomePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language Test Generator")
        self.resize(1000,700)
        self.language = None
        self.level = None
        self.size = None

        central = QWidget(self); self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.welcomePage = WelcomePage()
        self.langPage = BtnChoicePage(["Spanish", "French", "German", "Chinese", "Japanese", "Italian"],
                                      "Language",style = lang_page_style)
        self.levelPage = BtnChoicePage(["A1", "A2", "B1", "B2", "C1", "C2"],
                                       "Level", back_btn=True, style = level_page_style)
        self.sizePage = BtnChoicePage(["10","20","30"], "Test Size", back_btn=True,
                                      style = size_page_style)
        self.modePage = BtnChoicePage(['Words and Grammar', 'Reading', 'Listening'], "Test Mode",
                                      back_btn=True, style = mode_page_style)

        self.stack.addWidget(self.welcomePage)
        self.stack.addWidget(self.langPage)
        self.stack.addWidget(self.levelPage)
        self.stack.addWidget(self.sizePage)
        self.stack.addWidget(self.modePage)

        self.stack.setCurrentWidget(self.welcomePage)

        self.welcomePage.topic.connect(self._on_topic)
        self.langPage.info_selected.connect(self._on_language)
        self.levelPage.info_selected.connect(self._on_level)
        self.sizePage.info_selected.connect(self._on_size)
        self.modePage.info_selected.connect(self._on_mode)

        self.levelPage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.langPage))
        self.sizePage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.levelPage))
        self.modePage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.sizePage))

        self.test = {1:{"type": Qtyp.light, "question": "What is 2 + 2?", "right_answer": "4", "answers": ["3", "4", "5", "6"]},
                     2:{"type": Qtyp.medium, "question": "What is the capital of France?","right_answer": "Paris" ,"answers": ["Berlin", "Madrid", "Paris", "Rome"]},
                     3:{"type": Qtyp.hard, "question": "Solve the equation: 3x - 5 = 16", "right_answer": "7", "answers": []}}
        self.cur_index = 1
        self.score = 0
        self.max_score = sum([int(self.test[i]["type"]) + 1 for i in self.test])

    def create_question(self):
        self.prequestionPage = QuestionWaitPage(self.test[self.cur_index]["question"],2)
        self.questionPage = QuestionPage(self.test[self.cur_index]["type"],
                                         self.test[self.cur_index]["question"],
                                         self.test[self.cur_index]["answers"])
        self.stack.addWidget(self.prequestionPage)
        self.stack.addWidget(self.questionPage)
        self.stack.setCurrentWidget(self.prequestionPage)
        self.prequestionPage.ready.connect(self.start_question)
        self.questionPage.answer_selected.connect(self._answer_selected)

    def start_question(self):
        self.stack.setCurrentWidget(self.questionPage)
        self.questionPage.start_timer()

    def create_result(self):
        self.resPage = ResultPage(int(self.score / self.max_score * 100))
        self.stack.addWidget(self.resPage)
        self.stack.setCurrentWidget(self.resPage)

    def _answer_selected(self, ans):
        print("Selected answer:", ans)
        if ans == self.test[self.cur_index]["right_answer"]:
            self.score += int(self.test[self.cur_index]["type"]) + 1
        if self.cur_index < len(self.test):
            self.cur_index += 1
            self.create_question()
        else:
            self.create_result()

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
        self.stack.setCurrentWidget(self.modePage)
    def _on_mode(self, mode):
        self.mode = mode
        self.create_question()