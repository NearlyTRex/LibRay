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
import gzip

ORDER = 'big'
IRD_ORDER = 'little'
SECTOR = 2048

def bytes_to_int(byte):
  return int.from_bytes(byte, ORDER)

def ird_bytes_to_int(byte):
  return int.from_bytes(byte, IRD_ORDER)

def read_seven_bit_encoded_int(fileobj):
  # Read out an Int32 7 bits at a time. The high bit
  # of the byte when on means to continue reading more bytes
  count = 0
  shift = 0
  byte = -1
  while (byte & 0x80) != 0 or byte == -1:
    # Check for a corrupted stream. Read a max of 5 bytes.
    if shift == (5 * 7):
      raise ValueError
    byte = ird_bytes_to_int(fileobj.read(1))
    count |= (byte & 0x7F) << shift
    shift += 7
    print(byte, count, shift)
  return count


class IRD:

  def is_compressed(self, fileobj):
    fileobj.seek(0)
    return fileobj.read(4) != b"3IRD"

  def uncompress(self, filename):
    with gzip.open(filename, 'rb') as gzfile:
          with open('ird', 'wb') as outfile:
            outfile.write(gzfile.read())    

  def __init__(self, filename):
   
    with open(filename, 'rb') as fileobj:
      if self.is_compressed(fileobj):
        self.uncompress(filename)
    
    self.size = os.stat('ird').st_size
    with open('ird', 'rb') as ird:
      self.magic_string = ird.read(4)
      self.version = ird_bytes_to_int(ird.read(1))
      self.game_id = ird.read(9)
      length = read_seven_bit_encoded_int(ird)
      self.game_name = ird.read(length)
      self.update_version = ird.read(4)
      self.game_version = ird.read(5)
      self.app_version = ird.read(5)
      if self.version == 7:
        self.identifier = ird.read(4)
      if self.version < 9:
        back = ird.tell()
        length = read_seven_bit_encoded_int(ird)
        if length:
          self.header = ird.read(length)  
        else:
          ird.seek(back)
        back = ird.tell()
        length = read_seven_bit_encoded_int(ird)
        if length:
          self.footer = ird.read(length)
        else:
          ird.seek(back)
      self.region_count = ird_bytes_to_int(ird.read(1))
      self.region_hash = []
      for i in range(0, self.region_count):
        self.region_hash.append(ird.read(16))
      self.file_count = ird_bytes_to_int(ird.read(4))
      print(vars(self) )
      

      return
      sys.exit()
      back = ird.tell()
      prefix = bytes_to_int(ird.read(1))
      length = prefix >> 1
      if prefix & 0b00000001:
        ird.seek(back)

      

      
      self.header = ird.read(length)
      back = ird.tell()
      prefix = bytes_to_int(ird.read(1))
      length = prefix >> 1
      ird.seek(back)
      self.footer = ird.read(length)
      self.region_count
      
      print(self.game_name, self.update_version, self.game_version, self.region_count)

      ird.seek(self.size - (2 + 115 + 16 + 16))
      if self.version >= 9:
        self.pic = ird.read(115)
      self.data_one = ird.read(16)
      print(self.data_one.hex())
      self.data_two = ird.read(16)
      if self.version < 9:
        self.pic = ird.read(115)
      self.uid = ird.read(2)

      print(self.pic)
      print(self.uid)
      print(self.game_id)
    
    if filename != 'ird':
      os.remove('ird')



