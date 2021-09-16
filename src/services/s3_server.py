import boto3
import os

from services.server_types import ServerTypes


class FTPserver(ServerTypes):


    def upload(self,access_key, secret_access_key,bucket, path):

        client = boto3.client('s3',
                            aws_access_key_id= access_key,
                            aws_secret_access_key = secret_access_key)

        for file in os.listdir(path):

            if os.path.isfile(os.path.join(path, file)):
            
                filepath = path + '/' + file

                try:
                    upload_file_bucket = bucket
                    upload_file_key = filepath
                    client.upload_file(file, upload_file_bucket, upload_file_key)
                except(AssertionError):
                    pass
                else:
                    os.remove(filepath)
