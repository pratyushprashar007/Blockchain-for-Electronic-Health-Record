# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:26:39 2021

@author: Studio Pc-1
"""
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256
import random
import rsa
import binascii

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename+"enc"
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

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
	hasher = sha256(password.encode('utf-8'))
	return hasher.digest()

def Main():
    filename = '2.jpg'
    password = str(random.randint(1000,9999))
    
    publicKey, privateKey = rsa.newkeys(512)    
    
    print("private key string: ", type(privateKey))
    
    with open(filename+'_private.pem', 'w+') as keyfile:
        keyfile.write(str(privateKey))
        keyfile.close()
    
    encMessage = rsa.encrypt(password.encode(),publicKey)
    hexilify= binascii.hexlify(encMessage)
    
    # print("original string: ", password)
    
    str1 = hexilify.decode('UTF-8') 
    
    stringofdata=str1
    # print(str1)
    convertedtobyte = bytes(stringofdata, 'utf-8')
    # print(convertedtobyte)
    
    with open( filename+'_private.pem', 'r' ) as f:
        prikey = rsa.key(f.read())

    # print("Private key is this")
    print(type(prikey))
    
    # byte[] data = Base64.getDecoder().decode((prikey.getBytes()));
    # X509EncodedKeySpec spec = new X509EncodedKeySpec(data);
    # KeyFactory fact = KeyFactory.getInstance("RSA");
    # return fact.generatePublic(spec);
    
    decMessage = rsa.decrypt(binascii.unhexlify(convertedtobyte), prikey).decode()
     
    print("decrypted string: ", decMessage)


Main()