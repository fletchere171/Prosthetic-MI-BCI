# main.py
import sys
from PyQt6.QtWidgets import QApplication
from bci_app.ui.main_window import MainWindow
import qdarkstyle


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    win = MainWindow()
    win.resize(1000, 600)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
