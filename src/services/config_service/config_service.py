from services.config_service.contracts.configuration import  DB_Directory, DB_Destination
from services.config_service.repository.config_repository import ConfigRepository
from contracts.configuration import Directory, Destination

import keyring
import subprocess
import os

class ConfigService:

    def __init__(self):
        self.config_repository = ConfigRepository()  


    def loadAll(self):

        db_directories = self.config_repository.get_directories()
        db_destinations = self.config_repository.get_destinations()

        directories = []
        destinations = []

        for i in range(len(db_directories)):
            directory = Directory(db_directories[i].dirpath, db_directories[i].destination)
            directories.append(directory)

        for i in range(len(db_destinations)):
            destination = Destination(
                            db_destinations[i].ip, 
                            db_destinations[i].protocol, 
                            db_destinations[i].username)
            destinations.append(destination)


        to_load = {
            'directories': directories,
            'destinations': destinations
        }

        return to_load


    def loadQuery(self, for_query):

        if '/' in for_query:
            output = self.config_repository.get_directories(for_query)
            to_load = Directory(output.dirpath, output.destination)

        elif '.' in for_query:
            output = self.config_repository.get_destinations(for_query)
            to_load = Destination(
                            output.ip, 
                            output.protocol, 
                            output.username,
                            keyring.get_password(output.ip, output.username))

        return(to_load)


    def save(self, config):
    
        if 'Directory' in str(type(config)):
            to_save = DB_Directory(config.dirpath, config.destination)

        elif 'Destination' in str(type(config)):
            to_save = DB_Destination(config.ip, config.username, config.protocol)

            keyring.set_password(config.ip, config.username, config.password)

            if config.protocol == 'sftp':
                cmd = 'powershell.exe ssh-keyscan.exe -p 22 172.16.0.60'
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in p.stdout:
                    if b'ssh-rsa' in line:
                        home = os.environ['HOME']
                        with open(home + r"\known_hosts","a") as f:
                            f.write('sftpserver,' + line.decode("utf-8"))

        self.config_repository.save_row(to_save)


    def delete(self, to_delete):

        if '/' in to_delete:
            dataset_to_load = self.config_repository.get_directories(to_delete)

        elif '.' in to_delete:
            dataset_to_load = self.config_repository.get_destinations(to_delete)

        self.config_repository.delete(dataset_to_load)
