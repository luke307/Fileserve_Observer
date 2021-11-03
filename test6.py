import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QComboBox, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.auto = QComboBox(self)

        self.initUI()


    def initUI(self):

        self.comboBox1 = QComboBox(self)
        self.comboBox1.addItem('One')
        self.comboBox1.addItem('Two')

        self.comboBox1.currentTextChanged.connect(self._text_changed)

        self.auto.addItem('None')

        layout = QVBoxLayout()

        layout.addWidget(self.comboBox1)
        layout.addWidget(self.auto)

        self.setLayout(layout)
        self.show()

    def _text_changed(self):
        self.auto.addItem('Haus')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  