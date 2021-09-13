import ftplib
import pysftp
import os

from services.config_service.config_service import ConfigService

class UploadToServer:

    def __init__(self):
        pass


    def upload(self,ip, user, password, path, protocol):

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                if protocol == 'sftp':
                    with pysftp.Connection(ip, username=user, password=password) as sftp:
                        sftp.put(filepath)

                elif protocol == 'ftp':
                    ftp = ftplib.FTP(ip)
                    ftp.login(user, password)
                    ftp.storbinary(f'STOR {file}', open(filepath,'rb'))
                
                os.remove(filepath)
