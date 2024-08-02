from PyQt5.QtWidgets import QApplication
import sys

from welcome import MyWelcomeWindow


def window():
    app = QApplication(sys.argv)
    win = MyWelcomeWindow()
    win.setWindowTitle("VocabTest")
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
