from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os

from services.config_service.contracts.configuration import Base, DB_Directory, DB_Destination


class ConfigRepository:

    def __init__(self):

        path = os.getcwd()
        db = os.path.join(path, 'db\\ftpdb.db')

        _engine = create_engine('sqlite:///' + db)
        Base.metadata.create_all(bind=_engine)
        self._session = Session(_engine)


    def save_row(self, dataset):
        with self._session as session:
            session.add(dataset)
            session.commit()


    def delete(self, data):
        with self._session as session:
            session.delete(data)
            session.commit()


    def update_row(self, to_update):
        pass


    def get_directories(self, path_for_query = None):
        directories = None
        with self._session as session:
            if path_for_query:
                directories = session.query(DB_Directory).filter(DB_Directory.dirpath == path_for_query).first()
            else:
                directories = session.query(DB_Directory).all()

        return directories


    def get_destinations(self, ip_for_query = None):
        destinations = None
        with self._session as session:
            if ip_for_query:
                destinations = session.query(DB_Destination).filter(DB_Destination.ip == ip_for_query).first()
            else:
                destinations = session.query(DB_Destination).all()

        return destinations
    
