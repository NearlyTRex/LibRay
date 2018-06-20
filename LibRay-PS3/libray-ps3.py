#!/usr/bin/env python
# -*- coding: utf8 -*-

# LibRay-PS3 - Libre Blu-Ray PS3 ISO Tool
# Copyright (C) 2018 Nichlas Severinsen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import core
import struct
from Crypto.Cipher import AES


if __name__ == '__main__':
  print(os.path.getsize(sys.argv[1]))
  size = os.stat(sys.argv[1])  #.st_size.to_bytes(2, core.ORDER)
  print(size)
  with open(sys.argv[1], 'rb') as iso:
    sector1 = iso.read(core.SECTOR)
    num_unenc_sectors = int.from_bytes(sector1[0:4], core.ORDER)
    unknown = sector1[4:8]
    regions = []
    encrypted = False
    # TODO: I think I have a bug, these start and end addresses should be multiplied by 8?
    for i in range(0, (num_unenc_sectors*2)-1 ):
      regions.append({'start': sector1[8+4*i:12+4*i], 'end': sector1[12+4*i:16+4*i], 'enc': encrypted})
      encrypted = not encrypted

    regions.append({'start': regions[-1]['end'], 'end': size, 'enc': True})    

    # data1 from ird: 44 4901 0800 0020 0042 444f 0111 0101 00
    # TODO: import .ird (which can either be plaintext starting with 3IRD or .gz)
    
    data = bytes(bytearray.fromhex("444901080000200042444f0111010100"))
    key  = bytes(bytearray.fromhex("380bcf0b53455b3c7817ab4fa3ba90ed"))
    iv   = bytes(bytearray.fromhex("69474772af6fdab342743aefaa186287"))

    cipher = AES.new(key, AES.MODE_CBC, iv)
    disc_key = cipher.encrypt(data)
    print(disc_key)

    with open('output.iso', 'wb') as output:
      for region in regions:
        start = int(region["start"].hex(), 16)*2048
        end = int(region["end"].hex(), 16)*2048
        #start = int.from_bytes(region["start"], core.ORDER)*8
        #end = int.from_bytes(region["end"], core.ORDER)*8
        print(region)
        print('start: ', start)
        print('end: ', end)
        print('size: ', end - start - 1)
        if region['enc']:
          num = end
          print(num)
          iv = ['' for i in range(0,16)]
          for j in range(0,16):
            iv[16 - j - 1] = hex(ord(struct.pack("B", num & 0xFF))).replace('0x','')
            num >>= 8
    
          iv = "".join(iv)[-16:]
  
          iso.seek(start)
          data = iso.read(end - start - 1)
          print(len(data))
          cipher = AES.new(disc_key, AES.MODE_CBC, iv)
          output.write(cipher.decrypt(data))
          continue

        iso.seek(start)
        data = iso.read(end - start - 1)
        print(len(data))
        output.write(data)
  
    
    







