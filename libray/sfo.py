# -*- coding: utf8 -*-

# libray - Libre Blu-Ray PS3 ISO Tool
# Copyright © 2018 -2021 Nichlas Severinsen
#
# This file is part of libray.
#
# libray is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libray is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libray.  If not, see <https://www.gnu.org/licenses/>.


try:
  from libray import core
except ImportError:
  import core


class SFO:
  """Class for handling .sfo files

  Attributes:
    magic: Magic header
    version: .SFO version
    key_table_start: Absolute offset for key_table in .SFO
    data_table_start: Absolute offset for index_table in .SFO
    tables_entries: Number of entries in index_table and key_table
    key_data: Parsed keys and data tables from .SFO transformed into dict
  """

  def __init__(self, fp):

    self.file_start = fp.tell()

    # Header

    self.magic = fp.read(4)
    self.version = fp.read(4)
    self.key_table_start = core.to_int(fp.read(4), 'little')
    self.data_table_start = core.to_int(fp.read(4), 'little')
    self.tables_entries = core.to_int(fp.read(4), 'little')

    # Index table

    index_table = []

    for _ in range(0, self.tables_entries):
      index_table.append({
        'key_offset': core.to_int(fp.read(2), 'little'),
        'data_fmt': fp.read(2),
        'data_len': core.to_int(fp.read(4), 'little'),
        'data_max_len': core.to_int(fp.read(4), 'little'),
        'data_offset': core.to_int(fp.read(4), 'little'),
      })

    # Key table

    key_table = []

    for i in range(0, self.tables_entries):

      # Seek to absolute offset + relative offset of key

      fp.seek(self.file_start + self.key_table_start + index_table[i]['key_offset'])

      # Read key string until nullbyte

      key = ''

      while True:

        data = fp.read(1)

        if data == b'\x00':
          break

        key += data.decode('utf8')

      key_table.append(key)

    # Data table

    self.key_data = {}

    for i in range(0, self.tables_entries):

      # Seek to absolute offset + relative offset of data

      fp.seek(self.file_start + self.data_table_start + index_table[i]['data_offset'])

      if index_table[i]['data_fmt'] == b'\x04\x02': #UTF8
        data = fp.read(index_table[i]['data_len'] - 1).decode('utf8')
      elif index_table[i]['data_fmt'] == b'\x04\x04': #int32
        data = core.to_int(fp.read(index_table[i]['data_len']), 'little')
      else: # Meh
        data = fp.read(index_table[i]['data_len'])

      self.key_data[key_table[i]] = data


  def __getitem__(self, key):
    """Overload [] so we can directly select data using key from .SFO"""
    return self.key_data[key]


  def print_info(self):

    print('Magic:', self.magic)
    print('Version: ', self.version)
    print('key_table_start:', self.key_table_start)
    print('data_table_start:', self.data_table_start)
    print('tables_entries:', self.tables_entries)

    print(self.key_data)

