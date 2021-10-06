import sys
import time
import logging
import ntpath
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from services.config_service.config_service import ConfigService
from services.server_types import ServerTypes
from services.ftp_server import FTPserver
from services.sftp_server import SFTPserver
from services.s3_server import S3server


class Event(LoggingEventHandler):

    def on_created(self, event):

        filepath = event.src_path
        path = ntpath.dirname(filepath)
        config_service = ConfigService()
        directory = config_service.loadQuery(path)
        destination = config_service.loadQuery(directory.destination)

        uploadDir: ServerTypes
        print(destination.protocol,destination.protocol == 'otc',path)
        if destination.protocol == 'ftp':
            uploadDir = FTPserver()
        elif destination.protocol == 'sftp':
            uploadDir = SFTPserver()
        elif destination.protocol == 'otc':
            uploadDir = S3server()

        uploadDir.upload(destination.ip,destination.username,destination.password, path)


class MonitorService:

    def monitor(self):

        event_handler = Event()
        observer = Observer()

        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
            
        paths = []
        observers = []

        config_service = ConfigService()
        data = config_service.loadAll()
        directories = data['directories']

        for i in range(len(directories)):
            paths.append(directories[i].dirpath)
        
        for path in paths:
            observer.schedule(event_handler, path)
        
            observers.append(observer)
        
        observer.start()

        try:
            while True:
                time.sleep(1)
        finally:
            for o in observers:

                o.join()
