from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QStackedWidget, QLineEdit)
from screens.btn_choice_page import BtnChoicePage
from styles.btn_styles import lang_page_style, level_page_style, size_page_style, mode_page_style
from screens.result_page import ResultPage

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


        self.langPage = BtnChoicePage(["Spanish", "French", "German", "Chinese", "Japanese", "Italian"],
                                      "Language",style = lang_page_style)
        self.levelPage = BtnChoicePage(["A1", "A2", "B1", "B2", "C1", "C2"],
                                       "Level", back_btn=True, style = level_page_style)
        self.sizePage = BtnChoicePage(["10","20","30"], "Test Size", back_btn=True,
                                      style = size_page_style)
        self.modePage = BtnChoicePage(['Words and Grammar', 'Reading', 'Listening'], "Test Mode",
                                      back_btn=True, style = mode_page_style)

        self.stack.addWidget(self.langPage)
        self.stack.addWidget(self.levelPage)
        self.stack.addWidget(self.sizePage)
        self.stack.addWidget(self.modePage)


        self.langPage.info_selected.connect(self._on_language)
        self.levelPage.info_selected.connect(self._on_level)
        self.sizePage.info_selected.connect(self._on_size)
        self.modePage.info_selected.connect(self._on_mode)

        self.levelPage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.langPage))
        self.sizePage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.levelPage))
        self.modePage.back_requested.connect(lambda: self.stack.setCurrentWidget(self.sizePage))

        # test
        self.resPage = ResultPage(90)
        self.stack.addWidget(self.resPage)
        self.stack.setCurrentWidget(self.resPage)

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
        self.stack.setCurrentWidget(self.resPage)
        print("Chosen:", self.language, self.level, self.size, self.mode)