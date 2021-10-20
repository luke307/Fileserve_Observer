from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QComboBox, QTableWidgetItem, QMenu
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSlot, Qt

from services.process_service import ProcessService
from views.directory_window import DirectoryWindow
from services.config_service.config_service import ConfigService



##### Create Logger #####
import logging
import os

path = os.getcwd()
logpath = os.path.join(path, 'ftp.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler(logpath)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
###########################


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.config_service = ConfigService()
        self.config = None
        self.load_config()

        self._new_menu = DirectoryWindow(self.config['destinations'])
        #self._edit_menu = DirectoryWindow(config['destinations'],config['directories'],)

        new_button = QPushButton('new')
        new_button.clicked.connect(self._on_new_clicked)

        refresh_button = QPushButton('refresh')
        refresh_button.clicked.connect(self._on_refresh_clicked)

        activate_button = QPushButton('Activate')
        activate_button.clicked.connect(self._on_activate_clicked)

        kill_button = QPushButton('Kill')
        kill_button.clicked.connect(self._on_kill_clicked)

        comboBox = QComboBox(self)


        self.table = self.create_table()

        for i in range(len(self.config['directories'])):
            comboBox.addItem(self.config['directories'][i].dirpath)

        comboBox.setEditable(True)
        line_edit = comboBox.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()

        self.layout.addWidget(new_button)
        self.layout.addWidget(comboBox)
        self.layout.addWidget(refresh_button)
        self.layout.addWidget(activate_button)
        self.layout.addWidget(kill_button)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.show()


    def load_config(self) -> None:
        self.config = self.config_service.loadAll()

    def create_combobox(self):
        try:
            self.comboBox.clear()
        except AttributeError:
            pass
        self.comboBox = QComboBox(self)
        for i in range(len(self.config['directories'])):
            self.comboBox.addItem(self.config['directories'][i].dirpath)


    def create_table(self) -> QTableWidget:
        self.load_config()
        table = QTableWidget()
        table.setRowCount(len(self.config['directories']))
        table.setColumnCount(1)
        for i in range(len(self.config['directories'])):
            position_item = QTableWidgetItem()
            position_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable)

            table.setItem(i,0, QTableWidgetItem(self.config['directories'][i].dirpath))

        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self._create_context_menu)

        return table

    @pyqtSlot()
    def _on_new_clicked(self) -> None:
        self.load_config()
        self._new_menu = DirectoryWindow(self.config['destinations'])
        self._new_menu.show()


    @pyqtSlot()
    def _on_refresh_clicked(self) -> None:
        self.table.setParent(None)
        self.table = self.create_table()
        self.layout.addWidget(self.table)


    @pyqtSlot()
    def _on_activate_clicked(self) -> None:
        process_service = ProcessService()
        process_service.start()


    @pyqtSlot()
    def _on_kill_clicked(self) -> None:
        process_service = ProcessService()
        process_service.kill()

    @pyqtSlot()
    def _create_context_menu(self) -> None:
        position = QCursor.pos()
        context_menu = QMenu(self)
        action_edit = context_menu.addAction('Edit')
        action_delete = context_menu.addAction('Delete')

        action = context_menu.exec_(position)
        if action == action_edit:
            click_position = self.table.mapFromGlobal(position)
            item = self.table.itemAt(click_position)
            row = self.table.currentRow()
            if item != None and row > -1:
                self._edit_menu = DirectoryWindow(self.config['destinations'], item.text())
                self._edit_menu.show()
                self.table.setParent(None)
                self.table = self.create_table()
                self.layout.addWidget(self.table)

        if action == action_delete:
            click_position = self.table.mapFromGlobal(position)
            item = self.table.itemAt(click_position)
            row = self.table.currentRow()
            if item != None and row > -1:
                self.config_service.delete(item.text())
                self.table.removeRow(row)
