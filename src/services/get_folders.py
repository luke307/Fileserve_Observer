from ftplib import FTP
from pysftp import Connection
import boto3

class get_folders:

    def to_ftp(ip: str, user: str, password: str) -> list:

        with FTP(ip) as ftp:
            ftp.login(user, password)
            return ftp.dir()


    def to_sftp(ip: str, user: str, password: str) -> list:

        with Connection(ip, username=user, password=password) as sftp:
            return sftp.listdir()


    def to_otc(bucket: str, access_key: str, secret_access_key: str) -> list:

        client = boto3.client('s3',
                            aws_access_key_id= access_key,
                            aws_secret_access_key = secret_access_key,
                            endpoint_url='https://obs.eu-de.otc.t-systems.com')

        listObj = client.list_objects(Bucket= bucket, Delimiter= '/')
        return [f['Prefix'] for f in listObj['CommonPrefixes']]

if __name__=="__main__":
    pass
