# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 15:53:04 2021

@author: Studio Pc-1
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:32:00 2021

@author: Studio Pc-1
"""
import ipfsapi
import os
api = ipfsapi.Client(host='https://ipfs.infura.io', port=5001)


#new_file = api.add('2.jpg')
#print(new_file)

api.cat('QmWq6AfxDPp5DgfKiSZhxCNWECCEZ1FPEdErBkKwmvXHoY')