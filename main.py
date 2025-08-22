import sys
from app import App
from main_window import MainWindow

if __name__ == "__main__":
    app = App(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())