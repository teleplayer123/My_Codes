import os
import getpass
import sys
from hashlib import sha256

from encrypt_decrypt import encrypt, decrypt

"""
user = getpass.getuser()
if user != "username":
    sys.exit(1)
with open("secure.dat", "rb") as fh:
    password = pickle.loads(fh.read())
    print(password)
echo = getpass.getpass()
echo = sha256(echo.encode()).hexdigest()
if echo != password:
    sys.exit(1)
"""
filenames = sys.argv[1:]

def encrypt_file(filename):
    key = input("Enter secret key, remember this key as it will not be saved: ")
    chunk = 16 * 1024
    with open(filename, "r") as r:
        while True:
            data = r.read(chunk)
            if len(data) == 0:
                break
            with open(filename, "w") as w:
                w.write(encrypt(data, key))


def decrypt_file(filename):
    l = []
    key = input("Enter secret key: ")
    chunk = 16 * 1024
    with open(filename, "r") as r:
        while True:
            data = r.read(chunk)
            if len(data) == 0:
                break
            with open(filename, "w") as w:
                l.append(decrypt(data, key))
                w.write(decrypt(data, key))
    return l

for file in filenames:
    encrypt_file(file)
