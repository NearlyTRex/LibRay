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
import gzip

ORDER = 'big'
SECTOR = 2048

def bytes_to_int(byte):
  return int.from_bytes(byte, ORDER)

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
      self.version = bytes_to_int(ird.read(1))
      self.game_id = ird.read(9)
      self.game_name = ird.read(12)
      self.update_version = ird.read(4)
      self.game_version = ird.read(5)
      if self.version == 7:
        self.identifier = ird.read(4)
      self.header = ird.read(SECTOR*3)
      self.footer = ird.read(SECTOR)
      self.region_count = ird.read(1)
      
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

      print(self.uid)
    
    if filename != 'ird':
      os.rm('ird')



