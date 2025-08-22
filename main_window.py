from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QStackedWidget, QLineEdit)
from screens.size_page import SizePage
from screens.level_page import LevelPage
from screens.language_page import LanguagePage
from screens.mode_page import ModePage

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

        self.langPage = LanguagePage()
        self.levelPage = LevelPage()
        self.sizePage = SizePage()
        self.modePage = ModePage()

        self.stack.addWidget(self.langPage)
        self.stack.addWidget(self.levelPage)
        self.stack.addWidget(self.sizePage)
        self.stack.addWidget(self.modePage)

        self.langPage.language_selected.connect(self._on_language)
        self.levelPage.level_selected.connect(self._on_level)
        self.sizePage.size_selected.connect(self._on_size)
        self.modePage.mode_selected.connect(self._on_mode)

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
        print("Chosen:", self.language, self.level, self.size, self.mode)