import ftplib
import pysftp
import boto3
import os



class Upload:


    def to_ftp(self,ip, user, password, path):

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


    def to_sftp(self,ip, user, password, path):

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


    def to_otc(self,bucket, access_key, secret_access_key, path):

        client = boto3.client('s3',
                            aws_access_key_id= access_key,
                            aws_secret_access_key = secret_access_key,
                            endpoint_url='https://obs.eu-de.otc.t-systems.com')

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    upload_file_bucket = bucket
                    upload_file_key = 'LG_SDK_TEST/' + file
                    client.upload_file(filepath, upload_file_bucket, upload_file_key)
                except(AssertionError):
                    pass
                else:
                    os.remove(filepath)
