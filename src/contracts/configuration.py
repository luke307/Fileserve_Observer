class Directory:
    dirpath: str = ''
    destination: str = ''

    def __init__(self, dirpath, destination):
        self.dirpath = dirpath
        self.destination = destination


class Destination:
    ip: str = ''
    protocol: str = ''
    username: str = ''
    password: str = ''

    def __init__(self, ip, protocol, username, password = None):
        self.ip = ip
        self.username = username
        self.protocol = protocol
        self.password = password
