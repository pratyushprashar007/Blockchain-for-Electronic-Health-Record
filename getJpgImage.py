import ipfsapi
api = ipfsapi.Client(host='https://ipfs.infura.io', port=5001)

# new_file = api.add("2.jpg")
# print(new_file['Hash'],new_file['Name']) 
ipfs = "QmWq6AfxDPp5DgfKiSZhxCNWECCEZ1FPEdErBkKwmvXHoY"



# importing the module
from PIL import Image
import os
  
# importing the image 
im = Image.open(api.get(ipfs))
  
# converting to jpg
rgb_im = im.convert("RGB")
  
# exporting the image
rgb_im.save(ipfs+".jpg")