from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from services.config_service.contracts.configuration import Base, DB_Dataset, DB_Directory, DB_Destination


##### Create Logger #####
import logging
import os

path = os.getcwd()
logpath = os.path.join(path, 'ftp.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler(logpath)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
###########################


class ConfigRepository:

    def __init__(self):
        try:
            path = os.getcwd()
            if os.path.isdir(os.path.join(path,'db')):
                db = os.path.join(path, 'db/ftpdb.db')
            else:
                db = os.path.join(path, '../db/ftpdb.db')

            _engine = create_engine('sqlite:///' + db)
            Base.metadata.create_all(bind=_engine)
            self._session = Session(_engine)
        except:
            logger.exception('Can not connect to Database')


    def save_row(self, dataset: DB_Dataset) -> bool:
        try:
            with self._session as session:
                session.add(dataset)
                session.commit()

            for key in (key for key in vars(dataset) if not key.startswith('_')):
                logger.debug(key,': ', vars(dataset)[key])


            logger.info('Saved data to Database')
        except:
            logger.exception('Could not save data to Database')
            return False

        return True


    def delete(self, dataset: DB_Dataset) -> bool:
        try:
            with self._session as session:
                session.delete(dataset)
                session.commit()
    
            for key in (key for key in vars(dataset) if not key.startswith('_')):
                logger.debug(key,': ',vars(dataset)[key])

            logger.info('Deleted data from Database')
        except:
            logger.exception('Could not delete data from Database')
            return False

        return True


    def update_row(self, to_update: DB_Dataset) -> bool:
        pass


    def get_directories(self, path_for_query: str = None) -> DB_Directory:
        directories = None
        try:
            with self._session as session:
                if path_for_query:
                    directories = session.query(DB_Directory).filter(DB_Directory.dirpath == path_for_query).first()
                else:
                    directories = session.query(DB_Directory).all()

        except:
            logger.exception('Could not get Directories from Database')

        return directories


    def get_destinations(self, ip_for_query: str = None) -> DB_Destination:
        destinations = None
        try:
            with self._session as session:
                if ip_for_query:
                    destinations = session.query(DB_Destination).filter(DB_Destination.ip == ip_for_query).first()
                else:
                    destinations = session.query(DB_Destination).all()
        except:
            logger.exception('Could not get Destinations from Database')

        return destinations
