from cryptography.fernet import Fernet
import pathlib

key = Fernet.generate_key()
f = Fernet(key)

print(key)
password = input("insert password to encrypt:")
password = bytes(password, 'utf-8')
token = f.encrypt(password)
print(token)
path = pathlib.Path(__file__).parent.resolve()
path = str(path)

f = open(path + "\password-encryptet2.txt", "x")
token = str(token)
f.write(token)
f.close()