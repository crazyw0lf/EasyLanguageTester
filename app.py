from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setStyle("Fusion")
        self.setApplicationName("Language Test Generator")
        p = QPalette()
        p.setColor(QPalette.Window, QColor(30, 30, 30))
        p.setColor(QPalette.Base, QColor(22,22,22))
        p.setColor(QPalette.Button, QColor(70,70,70))
        p.setColor(QPalette.ButtonText, Qt.white)
        p.setColor(QPalette.Text, Qt.white)
        p.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(p)