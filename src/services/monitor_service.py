import sys
import time
import logging
import ntpath
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileSystemEvent
from services.config_service.config_service import ConfigService
from services.upload_functions import Upload


class Event(FileSystemEventHandler):

    def on_created(self, event: FileSystemEvent) -> None:

        filepath = event.src_path
        path = ntpath.dirname(filepath)
        config_service = ConfigService()
        directory = config_service.loadQuery(path)
        destination = config_service.loadQuery(directory.destination)

        
        match destination.protocol:
            case 'ftp':
                Upload.to_ftp(destination.ip,destination.username,destination.password, path, directory.serverdir)

            case 'sftp':
                Upload.to_sftp(destination.ip,destination.username,destination.password, path, directory.serverdir)

            case 'otc':
                Upload.to_otc(destination.ip,destination.username,destination.password, path, directory.serverdir)


class MonitorService:

    def monitor(self) -> None:

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
