import boto3
import os

from services.server_types import ServerTypes


class S3server(ServerTypes):


    def upload(self,bucket, access_key, secret_access_key, path):

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
