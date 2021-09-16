import ftplib
import os

from services.server_types import ServerTypes


class FTPserver(ServerTypes):


    def upload(self,ip, user, password, path, protocol):

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    ftp = ftplib.FTP(ip)
                    ftp.login(user, password)
                    ftp.storbinary(f'STOR {file}', open(filepath,'rb'))
                except(AssertionError):
                    pass
                else:
                    os.remove(filepath)
