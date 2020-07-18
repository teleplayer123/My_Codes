from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os
import struct
import getpass
import sys
from hashlib import sha256

from encrypt_decrypt import encrypt, decrypt
from utils import pad, unpad

"""
user = getpass.getuser()
if user != "csash":
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

def encrypt_file_data(filename):
    key = input("Enter secret key, remember this key as it will not be saved: ")
    def read_file(filename):
        chunk = 16 * 1024
        chunk -= chunk % 3
        with open(filename, "r") as r:
            while True:
                data = r.read(int(chunk))
                if len(data) == 0:
                    break
                yield data
    efile = filename[:-4] + "e" + filename[-4:]
    with open(efile, "w") as w:
        for data in read_file(filename):
            w.write(encrypt(data, key))


def decrypt_file_data(filename):
    key = input("enter secret key: ")
    filename = filename[:-4] + "e" + filename[-4:]
    def read_file():
        #chunk = (16 * 1024) / 3 * 4
        #chunk -= chunk % 4
        chunk = 21868
        with open(filename, "r") as r:
            while True:
                data = r.read(int(chunk))
                if len(data) == 0:
                    break
                yield data
    outfile = filename[:-5] + filename[-4:]
    with open(outfile, "w") as w:
        for data in read_file():
            w.write(decrypt(data, key))


def encrypt_file(filename):
    key = input("enter key: ")
    with open(filename, "r") as r:
        data = r.read()
        with open(filename, "w") as w:
            w.write(encrypt(data, key))

def decrypt_file(filename):
    key = input("enter key: ")
    with open(filename, "r") as r:
        data = r.read()
        with open(filename, "w") as w:
            w.write(decrypt(data, key))

running = True
for filename in filenames:
    while True:
        cmd = input("(e)ncrypt (d)ecrypt (q)uit\n" )
        if cmd in {"encrypt", "-encrypt", "e", "-e"}:
            encrypt_file_data(filename)
        elif cmd in {"decrypt", "-decrypt", "d", "-d"}:
            decrypt_file_data(filename)
        elif cmd in {"ee", "-ee"}:
            encrypt_file(filename)
        elif cmd in {"dd", "-dd"}:
            decrypt_file(filename)
        elif cmd in {"q", "-q"}:
            break
        else:
            sys.exit(0)
