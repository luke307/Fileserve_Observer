import os

#os.chdir('..')
path = os.getcwd()
db = os.path.join(path, 'db\\ftpdb.db')

print(db)