from sqlalchemy import Table, Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DB_Dataset(Base):
    __abstract__ = True


class DB_Directory(DB_Dataset):
    __tablename__ = "directories"

    dirpath = Column(String, primary_key=True)
    destination = Column(String)
    serverdir = Column(String)

    def __init__(self, dirpath, destination, serverdir):
        self.dirpath = dirpath
        self.destination = destination
        self.serverdir = serverdir


class DB_Destination(DB_Dataset):
    __tablename__ = "destinations"

    ip = Column(String, primary_key=True)
    username = Column(String)
    protocol = Column(String)

    def __init__(self, ip, username, protocol):
        self.ip = ip
        self.username = username
        self.protocol = protocol
