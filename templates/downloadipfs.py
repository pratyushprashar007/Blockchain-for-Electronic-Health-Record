import os
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256

from cryptography.fernet import Fernet

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "(enc)"+filename
    print("outputFile")
    print(outputFile)
    filesize = str(os.path.getsize(filename)).zfill(16)
    print('FILESIZE',filesize)
    IV = Random.new().read(16)
    print(IV)

    encryptor = AES.new(key, AES.MODE_CBC, IV)
    try:
        with open(filename, 'rb') as infile:#rb means read in binary
            with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk)%16 != 0:
                    chunk += b' '*(16-(len(chunk)%16))

                outfile.write(encryptor.encrypt(chunk))
    except Exception  as e:
        print("If there is ExceptionI, then execute this block.")

def decrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename[11:]
    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor= AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)

def getKey(password):
    hasher = sha256(password)
    return hasher.digest()

def Main():
    filename = '2.jpg'
    password = '1234' 
    print(password)
    
    encrypt(getKey(password), filename)
    print('Done.')

    decrypt(getKey(password),filename)
    print("Done.")



Main()