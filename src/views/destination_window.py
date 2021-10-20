from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QTableWidget, QComboBox, QMessageBox
from PyQt5.QtCore import pyqtSlot

from services.config_service.config_service import ConfigService
from contracts.configuration import Directory, Destination

class DestinationWindow(QWidget):

    def __init__(self, edit):

        super().__init__()

        self.config_service = ConfigService()

        ip_label = QLabel('IP')
        self.ip_input = QLineEdit()

        username_label = QLabel('Username')
        self.username_input = QLineEdit()

        password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self._on_save_clicked)

        if edit:
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(self._on_delete_clicked)

        box_label = QLabel('Protocol:')
        self.comboBox = QComboBox(self)
        self.comboBox.addItem('ftp')
        self.comboBox.addItem('sftp')
        self.comboBox.addItem('otc')

        layout = QVBoxLayout()

        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(box_label)
        layout.addWidget(self.comboBox)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)   
        layout.addWidget(save_button)
        if edit:
            layout.addWidget(delete_button)

        self.setLayout(layout)



    @pyqtSlot()
    def _on_save_clicked(self) -> None:

        newDes = Destination(
                    self.ip_input.text(), 
                    self.comboBox.currentText(),
                    self.username_input.text(), 
                    self.password_input.text()
                    )

        is_saved = self.config_service.save(newDes)
        if is_saved:
            output = 'Succesfully saved'
        else:
            output = 'Failed to save'

        message = QMessageBox.information(self, 'Information', output, QMessageBox.Ok)

        if is_saved:
            self.close()


    @pyqtSlot()
    def _on_delete_clicked(self) -> None:

        oldDes = Destination(
                    self.ip_input.text(), 
                    self.username_input.text(), 
                    self.password_input.text(), 
                    self.comboBox.currentText())

        is_deleted = self.config_service.save(oldDes)
        if is_deleted:
            output = 'Succesfully deleted'
        else:
            output = 'Failed to delete'

        message = QMessageBox.information(self, 'Information', output, QMessageBox.Ok)

        if is_deleted:
            self.close()
