# -*- coding: utf8 -*-

# libray - Libre Blu-Ray PS3 ISO Tool
# Copyright © 2018 - 2021 Nichlas Severinsen
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


import os
import sys
import stat
import zlib
import shutil
import requests
from bs4 import BeautifulSoup


try:
  from libray import iso
except ImportError:
  import iso

# Magic numbers / Constant variables

SECTOR = 2048
ALL_IRD_NET_LOC = 'http://jonnysp.bplaced.net/data.php'
GET_IRD_NET_LOC = 'http://jonnysp.bplaced.net/ird/'

# Utility functions


def to_int(data, byteorder='big'):
  """Convert bytes to integer"""
  if isinstance(data, bytes):
    return int.from_bytes(data, byteorder)


def to_bytes(data):
  """Convert a string of HEX to bytes"""
  if isinstance(data, str):
    return bytes(bytearray.fromhex(data))


ISO_SECRET = to_bytes("380bcf0b53455b3c7817ab4fa3ba90ed")
ISO_IV = to_bytes("69474772af6fdab342743aefaa186287")


def size(path):
  """Get size of a file or block device in bytes"""
  pathstat = os.stat(path)

  # Check if it's a block device

  if stat.S_ISBLK(pathstat.st_mode):
    return open(path, 'rb').seek(0, os.SEEK_END)

  # Otherwise, it's hopefully a file

  return pathstat.st_size


def read_seven_bit_encoded_int(fileobj, order):
  """Read an Int32, 7 bits at a time."""
  # The highest bit of the byte, when on, means to continue reading more bytes.
  count = 0
  shift = 0
  byte = -1
  while (byte & 0x80) != 0 or byte == -1:
    # Check for a corrupted stream. Read a max of 5 bytes.
    if shift == (5 * 7):
      raise ValueError
    byte = to_int(fileobj.read(1), order)
    count |= (byte & 0x7F) << shift
    shift += 7
  return count


def error(msg):
  """Print fatal error message and terminate"""
  print('[ERROR] %s' % msg)
  sys.exit(1)


def warning(msg, args):
  """Print a warning message. Warning messages can be silenced with --quiet"""

  if not args.quiet:
    print('[WARNING] %s. Continuing regardless.' % msg)


def vprint(msg, args):
  """Vprint, verbose print, can be silenced with --quiet"""

  if not args.quiet:
    print('[*] ' + msg)


def download_ird(ird_name):
  """Download an .ird from GET_IRD_NET_LOC"""

  # Check if file already exists and skip if it does
  if os.path.exists(ird_name): # TODO: might want to check that the file is valid first, could do a HEAD agains the url
    return

  ird_link = GET_IRD_NET_LOC + ird_name
  r = requests.get(ird_link, stream=True)

  with open(ird_name, 'wb') as ird_file:
    r.raw.decode_content = True
    shutil.copyfileobj(r.raw, ird_file)


def ird_by_game_id(game_id):
  """Using a game_id, download the responding .ird from ALL_IRD_NET_LOC"""
  gameid = game_id.replace('-','')
  try:
    r = requests.get(ALL_IRD_NET_LOC, headers = {'User-Agent': 'Anonymous (You)' }, timeout=5)
  except requests.exceptions.ReadTimeout:
    error('Server timed out, fix your connection or manually specify a key/ird.')
  soup = BeautifulSoup(r.text, "html.parser")

  ird_name = False
  for elem in soup.find_all("a"):
    url = elem.get('href').split('/')[-1].replace('\\"','')
    if gameid in url:
      ird_name = url

  if not ird_name:
    error("Unable to download IRD, couldn't find link. You could specify the decryption key with -d if you have it.")

  download_ird(ird_name)

  return(ird_name)


def crc32(filename):
  """Calculate crc32 for file"""

  with open(filename, 'rb') as infile:

    crc32 = 0

    while True:
      data = infile.read(65536)
      if not data:
        break
      crc32 = zlib.crc32(data, crc32)

    return "%08X" % (crc32 & 0xFFFFFFFF)


def serial_country(title):
  """Get country from disc serial / productcode / title_id"""

  if title[2] == 'A':
    return 'Asia'
  if title[2] == 'C':
    return 'China'
  if title[2] == 'E':
    return 'Europe'
  if title[2] == 'H':
    return 'Hong Kong'
  if title[2] == 'J' or title[2] == 'P':
    return 'Japan'
  if title[2] == 'K':
    return 'Korea'
  if title[2] == 'U':
    return 'USA'

  raise ValueError('Unknown country?!')


def multiman_title(title):
  """Fix special characters in title for Multiman style"""

  replace = {
    ':': ' -',
    '/': '-',
    '™': ' -',
  }

  for key, val in replace.items():
    title = title.replace(key, val)

  return title


# Main functions


def decrypt(args):
  """Try to decrypt a given .iso using relevant .ird or encryption key from argparse

  If no .ird is given this will try to automatically download an .ird file with the encryption/decryption key for the given game .iso
  """

  input_iso = iso.ISO(args)

  input_iso.decrypt(args) # TODO: some of the logic should probably be moved up here instead of residing in the decrypt function


def encrypt(args):
  """Try to re-encrypt a decrypted .iso using relevant .ird or encryption key from argparse

  If no .ird is given this will try to automatically download an .ird file with the encryption/decryption key for the given game .iso
  """

  input_iso = iso.ISO(args)

  input_iso.encrypt(args)
