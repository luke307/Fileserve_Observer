from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class DB_Dataset(Base):
    __abstract__ = True


@dataclass
class DB_Directory(DB_Dataset):
    __tablename__ = "directories"

    dirpath = Column(String, primary_key=True)
    destination = Column(String)


@dataclass
class DB_Destination(DB_Dataset):
    __tablename__ = "destinations"

    ip = Column('ip', String, primary_key=True)
    username = Column('username', String)
    protocol = Column('protocol', String)
