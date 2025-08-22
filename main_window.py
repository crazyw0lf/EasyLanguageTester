from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QStackedWidget, QLineEdit)
from screens.work_page import WorkPage
from screens.level_page import LevelPage
from screens.language_page import LanguagePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Language Test Generator")
        self.resize(1000,700)
        self.language = None
        self.level = None

        central = QWidget(self); self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.langPage = LanguagePage()
        self.levelPage = LevelPage()
        self.workPage = WorkPage()

        self.stack.addWidget(self.langPage)
        self.stack.addWidget(self.levelPage)
        self.stack.addWidget(self.workPage)

        self.langPage.language_selected.connect(self._on_language)
        self.levelPage.level_selected.connect(self._on_level)

    def _on_language(self, lang):
        self.language = lang
        self.stack.setCurrentWidget(self.levelPage)
    def _on_level(self, level):
        self.level = level
        self.stack.setCurrentWidget(self.workPage)
        print("Chosen:", self.language, self.level)