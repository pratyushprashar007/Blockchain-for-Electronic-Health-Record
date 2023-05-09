# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 12:29:37 2022

@author: Studio Pc-1
"""
import ipfsapi
api = ipfsapi.Client(host='https://ipfs.infura.io', port=5001)

new_file = api.add("2.jpg")
print(new_file['Hash'])  