from logging import Formatter
import sys
from PyQt5.QtWidgets import QApplication

from views.main_window import MainWindow

 
def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
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
    

    try:
        main()
    except:
        logger.exception('Failed to open the main Window')
