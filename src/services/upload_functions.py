from ftplib import FTP
from pysftp import Connection
import boto3


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


class Upload:

    def to_ftp(ip: str, user: str, password: str, path: str, serverdir: str) -> None:

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    with FTP(ip) as ftp:
                        ftp.login(user, password)
                        if serverdir:
                            ftp.cwd(serverdir)
                        ftp.storbinary(f'STOR {file}', open(filepath,'rb'))
                        
                except:
                    logger.exception("Could not upload to FTP-Server")
                else:
                    os.remove(filepath)
                    logger.info(f"Uploaded {filepath} to {ip}")


    def to_sftp(ip: str, user: str, password: str, path: str, serverdir: str) -> None:

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    with Connection(ip, username=user, password=password) as sftp:
                        if serverdir:
                            with sftp.cd(serverdir):
                                sftp.put(filepath)
                        else:
                            sftp.put(filepath)

                except:
                    logger.exception("Could not upload to SFTP-Server")
                else:
                    os.remove(filepath)
                    logger.info(f"Uploaded {filepath} to {ip}")


    def to_otc(bucket: str, access_key: str, secret_access_key: str, path: str, serverdir: str) -> None:

        client = boto3.client('s3',
                            aws_access_key_id= access_key,
                            aws_secret_access_key = secret_access_key,
                            endpoint_url='https://obs.eu-de.otc.t-systems.com')

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    upload_file_bucket = bucket
                    if serverdir:
                        upload_file_key = serverdir + file
                    else:
                        upload_file_key =  file
                    client.upload_file(filepath, upload_file_bucket, upload_file_key)
                except:
                    logger.exception("Could not upload to OTC")
                else:
                    os.remove(filepath)
                    logger.info(f"Uploaded {filepath} to {bucket}")
