from services.config_service.contracts.configuration import  DB_Directory, DB_Destination
from services.config_service.repository.config_repository import ConfigRepository
from contracts.configuration import Dataset, Directory, Destination
from dataclasses import dataclass

import keyring
import subprocess
import os

class ConfigService:

    def __init__(self):
        self.config_repository = ConfigRepository()  


    def loadAll(self) -> dict:
        '''loads the tables destination and directories in a dictionary with two lists of objects
        '''

        db_directories = self.config_repository.get_directories()
        db_destinations = self.config_repository.get_destinations()

        directories = []
        destinations = []

        for i in range(len(db_directories)):
            directory = Directory(
                            db_directories[i].dirpath,
                            db_directories[i].destination,
                            db_directories[i].serverdir)
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


    def loadQuery(self, for_query: str) -> Dataset:
        '''the function assumes that everything that has a slash in it is a file path 
        and everything which does not have a slash is a destination'''

        if '/' in for_query:
            output = self.config_repository.get_directories(for_query)
            to_load = Directory(
                            output.dirpath,
                            output.destination,
                            output. serverdir)

        else:
            output = self.config_repository.get_destinations(for_query)
            to_load = Destination(
                            output.ip, 
                            output.protocol, 
                            output.username,
                            keyring.get_password(output.ip, output.username))

        return(to_load)


    def save(self, config: Dataset) -> bool:
        '''in case of a new directory it just does an update in the directories table,
        in case of a new destination it saves the password via keyring
        if the protocol is sftp it gets a public key and saves the key localy'''
    
        if 'Directory' in str(type(config)):
            to_save = DB_Directory(
                            config.dirpath,
                            config.destination,
                            config.serverdir)

        elif 'Destination' in str(type(config)):
            to_save = DB_Destination(config.ip, config.username, config.protocol)

            keyring.set_password(config.ip, config.username, config.password)

            if config.protocol == 'sftp':
                cmd = f'powershell.exe ssh-keyscan.exe -p 22 {config.ip}'
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                for line in p.stdout:
                    if b'ssh-rsa' in line:
                        home = os.environ['HOME']
                        with open(home + r"\known_hosts","a") as f:
                            f.write('sftpserver,' + line.decode("utf-8"))

        is_saved = self.config_repository.save_row(to_save)
        return is_saved


    def delete(self, to_delete: Dataset) -> bool:
        '''the function assumes that everything that has a slash in it is a file path 
        and everything which does not have a slash is a destination'''

        if '/' in to_delete:
            dataset_to_load = self.config_repository.get_directories(to_delete)

        else:
            dataset_to_load = self.config_repository.get_destinations(to_delete)

        is_deleted = self.config_repository.delete(dataset_to_load)
        return is_deleted
