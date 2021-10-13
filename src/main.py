import sys
from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow


def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
