# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:32:00 2021

@author: Studio Pc-1
"""
import ipfsapi
import os
api = ipfsapi.Client(host='https://ipfs.infura.io', port=5001)

new_file = api.add(os.path.join('static/files/', 'a', 'Screenshot_60.png'))
print(new_file)