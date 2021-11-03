from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, Qt

import ntpath

from views.destination_window import DestinationWindow
from services.config_service.config_service import ConfigService
from services.get_folders import get_folders
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
        self.directory = directory


        self._new_menu = DestinationWindow(False)
        self._edit_menu = DestinationWindow(True)

        self.init_ui()


    def init_ui(self):

        path_to_directory_label = QLabel('Directory')
        self.path_to_directory_input = QLineEdit()

        browse_button = QPushButton('browse')
        browse_button.clicked.connect(self._on_browse_clicked)

        new_button = QPushButton('New Destination')
        new_button.clicked.connect(self._on_new_clicked)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self._on_save_clicked)


        self.comboBox_Des = QComboBox(self)
        for i in range(len(self.destination)):
            self.comboBox_Des.addItem(self.destination[i].ip)

        self.comboBox_Des.currentTextChanged.connect(self._modify_combobox)

        #box_label = QLabel('Directory:')
        self.comboBox_Dir = QComboBox(self)
        self._modify_combobox()

        layout = QVBoxLayout()

        layout.addWidget(path_to_directory_label)
        layout.addWidget(self.path_to_directory_input)
        layout.addWidget(browse_button)
        layout.addWidget(self.comboBox_Des)
        layout.addWidget(self.comboBox_Dir)
        layout.addWidget(new_button)
        layout.addWidget(save_button)


        if self.directory:
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(self._on_delete_clicked)
            layout.addWidget(delete_button)
            self.path_to_directory_input.setText(self.directory)

        self.setLayout(layout)

    @pyqtSlot()
    def _modify_combobox(self):

        self.comboBox_Dir.clear()
        self.comboBox_Dir.addItem('None')

        destination = self.config_service.loadQuery(self.comboBox_Des.currentText())

        match destination.protocol:
            case 'ftp':
                dir_list = get_folders.to_ftp(destination.ip,destination.username,destination.password)
            case 'sftp':
                dir_list = get_folders.to_sftp(destination.ip,destination.username,destination.password)
            case 'otc':
                dir_list = get_folders.to_otc(destination.ip,destination.username,destination.password)


        for i in range(len(dir_list)):
            self.comboBox_Dir.addItem(dir_list[i])


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

        newDir = Directory(
                    self.path_to_directory_input.text(),
                    self.comboBox_Des.currentText(),
                    self.comboBox_Dir.currentText())

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
