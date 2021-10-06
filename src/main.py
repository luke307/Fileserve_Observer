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

    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    # file_handler = logging.FileHandler('C:/Users/DE1119189/Desktop/Github/Fileserve_Observer/ftp.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    logging.basicConfig(filename='C:/Users/DE1119189/Desktop/Github/Fileserve_Observer/ftp.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(message)s')


    try:
        main()
    except:
        logging.exception('Failed to open the main Window')
