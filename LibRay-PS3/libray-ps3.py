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
import base64
import struct
import shutil
import binascii
from Crypto.Cipher import AES

def bytes_to_int(byte):
  return int.from_bytes(byte, core.ORDER)

def int_to_hexstr(integer):
  return '{:02x}'.format(integer)

def int_to_bytes(integer):
  return bytes(bytearray.fromhex(int_to_hexstr(integer)))

def hexstr_to_bytes(hexstr):
  return bytes(bytearray.fromhex(hexstr))

def bprint(byte):
  byteint = bytes_to_int(byte)
  print(byte, '\t->', byteint, '\t->', byteint*8, '\t->', byteint*2048 )

def decode(self, text):
    '''
    Remove the PKCS#7 padding from a text string
    '''
    nl = len(text)
    val = int(binascii.hexlify(text[-1]), 16)
    if val > self.k:
        raise ValueError('Input is not padded or padding is corrupt')

    l = nl - val
    return text[:l]


BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

if __name__ == '__main__':
  
  #core.IRD('BCAS20001-CA107E13820801F29488EBEB7D82A2C4.ird')
  #core.IRD('BLES00048-1AA29AD85F7770BDCED0B7030067D59A.ird')
  #sys.exit()
  
  bprint(b'\x00\x00\x00\x00')
  bprint(b'\x00\x00\x0c\xbf')
  bprint(b'\x00\x00\x00q\xc2')
  bprint(b'\x00\x00s\xc2\x7f')
  bprint(b'\x00\x00s\xc2\x80')

  data = hexstr_to_bytes("11089487d46ec9c1ec71205c2a6e8adc")
  key  = hexstr_to_bytes("380bcf0b53455b3c7817ab4fa3ba90ed")
  iv   = hexstr_to_bytes("69474772af6fdab342743aefaa186287")

  cipher = AES.new(key, AES.MODE_CBC, iv)
  disc_key = cipher.encrypt(data)
  print(disc_key)
  print(disc_key.hex())
  disc_key = hexstr_to_bytes("01AD4F9DFED22E37998BDDC57E135935")
  print(disc_key.hex())
  print(unpad(disc_key.hex()))
  disc_key = hexstr_to_bytes("DCD55A55B033905C58E7FE2A7F969F27")

  regions = [
    {'start': 0, 'end': 6682624, 'enc': False},
    {'start': 6682624, 'end': 59641856, 'enc': True},
    {'start': 59641856, 'end': 15537010688, 'enc': False},
    {'start': 15537010688, 'end': 15537012736, 'enc': True }
    # There's also a last sector between 15537010688 and 15537012736, but seems like it's not used
  ]

  files = []
  test = hexstr_to_bytes("70c2a1")
  with open(sys.argv[1], 'rb') as iso:
    for i, region in enumerate(regions):
      files.append('region_' + str(i))
      with open('region_' + str(i), 'wb') as output:
        iso.seek(region['start'])

        if not region['enc']:
          while iso.tell() < region['end']:
            data = iso.read(core.SECTOR)
            output.write(data)
          continue
        else:
          while iso.tell() < region['end']:
            data = iso.read(core.SECTOR)
            num = iso.tell()
            iv = bytearray([0 for i in range(0,16)])
            for j in range(0,16):
              iv[16 - j - 1] = (num & 0xFF) 
              num >>= 8
            
            cipher = AES.new(disc_key, AES.MODE_CBC, bytes(iv))
            decrypted = cipher.decrypt(data)

            if test in decrypted:
              print(iv.hex())
              print(data.hex())
              print(decrypted.hex())

            output.write(decrypted)
        print(iso.tell())
    

  with open('output.iso', 'wb') as iso:
    for f in files:
      with open(f, 'rb') as fd:
        shutil.copyfileobj(fd, iso, 1024*1024*10)
    
  sys.exit()

  size = os.stat(sys.argv[1]).st_size
  size_hex = bytes(bytearray.fromhex(hex(int(size / 2048)).replace('0x','').zfill(16)))

  print(size, size_hex)

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

    regions.append({'start': regions[-1]['end'], 'end': size_hex, 'enc': True})    
    print(regions)
    # data1 from ird: 44 4901 0800 0020 0042 444f 0111 0101 00
    # TODO: import .ird (which can either be plaintext starting with 3IRD or .gz)
    

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
  
    
    




