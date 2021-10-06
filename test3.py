import logging
#import logging.handlers
#import os
 
# handler = logging.handlers.WatchedFileHandler(
#     os.environ.get("LOGFILE","C:/Users/DE1119189/Desktop/Github/Fileserve_Observer/ftp.log"))
# formatter = logging.Formatter(logging.BASIC_FORMAT)
# handler.setFormatter(formatter)
# root = logging.getLogger()
# root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
# root.addHandler(handler)
 
logging.basicConfig(filename='C:/Users/DE1119189/Desktop/Github/Fileserve_Observer/ftp.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(message)s')

try:
    exit(main())
except Exception:
    logging.exception("Exception in main()")
    exit(1)