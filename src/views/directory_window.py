from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

import ntpath

from views.destination_window import DestinationWindow
from services.config_service.config_service import ConfigService
from contracts.configuration import Directory, Destination


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


class DirectoryWindow(QWidget):

    def __init__(self, destination: list, directory: Directory = None):

        super().__init__()

        self.config_service = ConfigService()
        self.destination = destination


        self._new_menu = DestinationWindow(False)
        self._edit_menu = DestinationWindow(True)


        path_to_directory_label = QLabel('Directory')
        self.path_to_directory_input = QLineEdit()

        browse_button = QPushButton('browse')
        browse_button.clicked.connect(self._on_browse_clicked)

        new_button = QPushButton('New Destination')
        new_button.clicked.connect(self._on_new_clicked)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self._on_save_clicked)


        self.comboBox = QComboBox(self)
        for i in range(len(destination)):
            self.comboBox.addItem(destination[i].ip)

        self.comboBox.setEditable(True)
        line_edit = self.comboBox.lineEdit()
        line_edit.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()

        layout.addWidget(path_to_directory_label)
        layout.addWidget(self.path_to_directory_input)
        layout.addWidget(browse_button)
        layout.addWidget(self.comboBox)
        layout.addWidget(new_button)    
        layout.addWidget(save_button)

        if directory:
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(self._on_delete_clicked)
            layout.addWidget(delete_button)
            self.path_to_directory_input.setText(directory)

        self.setLayout(layout)

    def create_combobox(self):
        try:
            self.comboBox.clear()
        except AttributeError:
            pass
        self.comboBox = QComboBox(self)
        for i in range(len(self.destination)):
            self.comboBox.addItem(self.destination[i].ip)

    @pyqtSlot()
    def _on_browse_clicked(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder  = QFileDialog.getExistingDirectory(self, 'Select a directory')
        if folder:
            self.path_to_directory_input.setText(folder)


    @pyqtSlot()
    def _on_new_clicked(self) -> None:
        self.close()
        self._new_menu.show()


    @pyqtSlot()
    def _on_save_clicked(self) -> None:

        newDir = Directory(self.path_to_directory_input.text(), self.comboBox.currentText())

        logger.debug(f'SAVE: path to directory:{newDir.dirpath}')
        logger.debug(f'SAVE: destination:{newDir.destination}')

        is_saved = self.config_service.save(newDir)
        if is_saved:
            output = 'Succesfully saved'
        else:
            output = 'Failed to save'

        QMessageBox.information(self, 'Information', output, QMessageBox.Ok)
        if is_saved:
            self.close()


    @pyqtSlot()
    def _on_delete_clicked(self) -> None:

        oldDir = Directory(self.path_to_directory_input.text(), self.comboBox.currentText())

        logger.debug(f'DELETE: path to directory:{oldDir.dirpath}')
        logger.debug(f'DELETE: destination:{oldDir.destination}')

        is_deleted = self.config_service.delete(oldDir)
        if is_deleted:
            output = 'Succesfully deleted'
        else:
            output = 'Failed to delete'

        QMessageBox.information(self, 'Information', output, QMessageBox.Ok)
        if is_deleted:
            self.close()
