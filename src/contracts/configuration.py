from dataclasses import dataclass


@dataclass
class Dataset:
    pass


@dataclass
class Directory(Dataset):
    dirpath: str = ''
    destination: str = ''


@dataclass
class Destination(Dataset):
    ip: str = ''
    protocol: str = ''
    username: str = ''
    password: str = ''
