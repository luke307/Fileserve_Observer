from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DB_Directory(Base):
    __tablename__ = "directories"

    dirpath = Column(String, primary_key=True)
    destination = Column(String)

    def __init__(self, dirpath, destination):
        self.dirpath = dirpath
        self.destination = destination


class DB_Destination(Base):
    __tablename__ = "destinations"

    ip = Column('ip', String, primary_key=True)
    username = Column('username', String)
    protocol = Column('protocol', String)

    def __init__(self, ip, username, protocol):
        self.ip = ip
        self.username = username
        self.protocol = protocol
