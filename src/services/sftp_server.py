import pysftp
import os

from services.server_types import ServerTypes


class FTPserver(ServerTypes):


    def upload(self,ip, user, password, path):

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    with pysftp.Connection(ip, username=user, password=password) as sftp:
                        sftp.put(filepath)

                except(AssertionError):
                    pass
                else:
                    os.remove(filepath)
