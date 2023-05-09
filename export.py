import rsa

publicKey, privateKey = rsa.newkeys(1024) 
print(privateKey)

with open('static/keys/master_private.pem', 'w+') as keyfile:
    keyfile.write(str(privateKey))
    keyfile.close()
        
    
with open('static/keys/master_public.pem', 'w+') as keyfile:
    keyfile.write(str(publicKey))
    keyfile.close()