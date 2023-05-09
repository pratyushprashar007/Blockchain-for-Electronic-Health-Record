from flask import Flask, flash, session, redirect
from flask import render_template,request,send_file
from werkzeug.utils import secure_filename
import os
import pathlib
import random
import pymysql
from Crypto.PublicKey import RSA

import ipfsapi
# api = ipfsApi.Client(host='https://ipfs.infura.io', port=5001)
api = ipfsapi.Client(host='127.0.0.1', port=5001)

#Importing necessary modules
from Crypto.Cipher import PKCS1_OAEP
from binascii import hexlify

from flask import send_from_directory
import base64

import binascii
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256

from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'any random string'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/main')
def main():
    return render_template('index1.html') 

@app.route('/logout')
def logout():
    session.pop('name',None)
    return render_template('index.html') 

@app.route('/SessionHandle',methods=['POST','GET'])
def SessionHandle():
    if request.method == "POST":
        details = request.form
        name = details['name']
        session['name'] = name
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser
    
@app.route('/ProvideKey')
def ProvideKey():
    return render_template('providekey.html') 

@app.route('/Addrecord')
def Addrecord():
    return render_template('addRecord.html')

@app.route('/Viewrecord')
def Viewrecord():
    return render_template('viewRecord.html') 

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename.split('.', 1)[0]+"enc.jpg"
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

def decrypt11(key, filename):
    chunksize = 64*1024
    outputFile = "static/decrypted//"+"dnc"+filename
    print('FILEIS',outputFile)
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


@app.route('/Uploadfile',methods=['POST','GET'])
def Uploadfile():
    if request.method == "POST":
        username = session.get("name")
        f2= request.files['file']
        print(f2)
        filename_secure = secure_filename(f2.filename)
        pathlib.Path(app.config['UPLOAD_FOLDER'], username).mkdir(exist_ok=True)
        print("print saved")
        f2.save(os.path.join(app.config['UPLOAD_FOLDER'], username, filename_secure))
        filename1 =os.path.join(app.config['UPLOAD_FOLDER'], username, filename_secure)        
        filename55 = filename_secure
        print(filename55)
        
        key = RSA.generate(2048)
        
        with open('static/keys/'+filename55.split('.', 1)[0]+'_private.pem', 'wb' ) as f:
            f.write( key.exportKey( 'PEM' ))
            
        filename = filename1
        password = str(random.randint(1000,9999))
        print(password)
    
        encrypt(getKey(password), filename) 
        
        publicKey = PKCS1_OAEP.new( key )
        secret_message = bytes(password, 'utf-8')
        
        encMessage = publicKey.encrypt( secret_message ) 
        hexilify= binascii.hexlify(encMessage)
        strencry = str(hexilify.decode('UTF-8'))
            
        new_file = api.add(os.path.join(app.config['UPLOAD_FOLDER'], username, filename55.split('.', 1)[0]+"enc.jpg"))
        print(new_file['Hash'],new_file['Name'])                      
        
        ListOfFile = {'a':filename55,'b':username,'c':filename55.split('.', 1)[0]+'_private.pem',
                      'd':strencry,'e': "public_key",'f':new_file['Hash']}
        return ListOfFile 
    return render_template('uploadFile.html',data={})

@app.route('/Download')
def Download():
    username = session.get("name")
    print(username)
    return render_template('download.html',username=username)

@app.route('/Sharefile',methods=['POST','GET'])
def Sharefile():
    if request.method == "POST":
        details = request.form        
        filename5 = details['filename']
        username55 = session.get("name")
        data = {'a':filename5,'b':username55}
        print(data)       
        
        return render_template('shareFile.html',data=data)
    return render_template('shareFile.html')

@app.route('/Receivedfiles',methods=['POST','GET'])
def Receivedfiles():
    username = session.get("name")
    print(username)
    return render_template('receivedfiles.html',username=username)

@app.route('/DownloadFile',methods=['POST','GET'])
def DownloadFile():
    if request.method == "POST":
        details = request.form        
        filename55 = details['filename']
        pri = details['privatekey']
        encry = details['encryptedkey']
        pub = details['publickey']
        ipfs = details['ipfs']
        username = session.get("name")
        
        with open( "static/keys/"+pri,'r' ) as f:
            key = RSA.importKey( f.read() )
        
        str1 = encry 
        convertedtobyte = bytes(str1, 'utf-8')
        public_crypter =  PKCS1_OAEP.new( key )
        decrypted_data = public_crypter.decrypt( binascii.unhexlify(convertedtobyte) )
        print(decrypted_data)
        str1 = decrypted_data.decode('UTF-8') 
        print(str1)        
        print(type(ipfs))
        
        print(str1)
        
        import urllib3
        url = 'http://127.0.0.1:8080/ipfs/'+ipfs
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET',url )
        f = open(ipfs, 'wb')
        f.write(resp.data)
        f.close()
        resp.release_conn()
        
        decrypt11(getKey(str(str1)) , ipfs)
        outputFilename = "static/decrypted//"+"dnc"+ipfs
        
        # decrypt(getKey(str1),ipfs)        
        return render_template('downloaddisplay.html',username=username,filetodisplay=outputFilename)
    return render_template('download.html',username=username)

@app.route('/DownloadFile1',methods=['POST','GET'])
def DownloadFile1():
    if request.method == "POST":
        details = request.form        
        filename55 = details['filename']
        uploader = details['uploader']
        pri = details['privatekey']
        ipfs = details['ipfs']
        encry = details['encryptedkey']
        username = session.get("name")
        print(uploader)
        print(details)     

        with open( "static/keys/"+pri,'r' ) as f:
            key = RSA.importKey( f.read() )
        
        str1 = encry 
        convertedtobyte = bytes(str1, 'utf-8')
        public_crypter =  PKCS1_OAEP.new( key )
        decrypted_data = public_crypter.decrypt( binascii.unhexlify(convertedtobyte) )
        print(decrypted_data)
        str1 = decrypted_data.decode('UTF-8') 
        print(str1)        
        print(type(ipfs))
        
        print(str1)
        
        import urllib3
        url = 'http://127.0.0.1:8080/ipfs/'+ipfs
        connection_pool = urllib3.PoolManager()
        resp = connection_pool.request('GET',url )
        f = open(ipfs, 'wb')
        f.write(resp.data)
        f.close()
        resp.release_conn()
        
        decrypt11(getKey(str(str1)) , ipfs)
        outputFilename = "static/decrypted//"+"dnc"+ipfs
        
        return render_template('downloaddisplay.html',username=username,filetodisplay=outputFilename)
    return render_template('receivedfiles.html',username=username)

if __name__ == "__main__":
    app.run("0.0.0.0")