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


import sys
import sqlite3
import pathlib
import pkg_resources
from tqdm import tqdm
from Crypto.Cipher import AES


try:
  from libray import core
  from libray import ird
  from libray import sfo
except ImportError:
  import core
  import ird
  import sfo


class ISO:
  """Class for handling PS3 .iso files.

  Attributes:
    size:              Size of .iso in bytes
    number_of_regions: Number of regions in the .iso
    regions:           List with info of every region
    game_id:           PS3 game id
    ird:               IRD object (see ird.py)
    disc_key:          data1 from .ird, encrypted
  """


  NUM_INFO_BYTES = 4


  def read_regions(self, input_iso, filename):
    """List with info dict (start, end, whether it's encrypted) for every region.

    Basically, every other (odd numbered) region is encrypted.
    """
    regions = []

    encrypted = False
    for _ in range(0, self.number_of_regions):

      regions.append({
        'start': core.to_int(input_iso.read(self.NUM_INFO_BYTES)) * core.SECTOR,
        'end': core.to_int(input_iso.read(self.NUM_INFO_BYTES)) * core.SECTOR,
        'enc': encrypted
      })

      input_iso.seek(input_iso.tell() - self.NUM_INFO_BYTES)

      encrypted = not encrypted

    # Last region might not actually be 2048 bytes, so we'll just cheat
    regions[-1]['end'] = self.size

    return regions


  def __init__(self, args):
    """ISO constructor using args from argparse."""

    self.size = core.size(args.iso)

    if not self.size:
      core.error('looks like ISO file/mount is empty?')

    with open(args.iso, 'rb') as input_iso:
      # Get number of regions (times two as the number represents both encrypted and decrypted regions  )
      self.number_of_regions = core.to_int(input_iso.read(self.NUM_INFO_BYTES)) * 2

      # Skip unused bytes
      input_iso.seek(input_iso.tell() + self.NUM_INFO_BYTES)

      self.regions = self.read_regions(input_iso, args.iso)

      # Seek to the start of sector 2, '+ 16' skips a section containing some 'playstation'
      input_iso.seek(core.SECTOR + 16)

      self.game_id = input_iso.read(16).decode('utf8').strip()

      # Find PARAM.SFO

      core.vprint('Searching for PARAM.SFO', args)

      input_iso.seek(0)
      counter = 1
      found_param = False

      while True:

        data = input_iso.read(8)

        if not data:
          break

        #if data == b'PS3LICDA':
        #  print(data)

        if data[0:4] == b'\x00\x50\x53\x46':
          found_param = True

          #input_iso.seek(input_iso.tell() - 8)
          #param = sfo.SFO(input_iso)
          #print(param['TITLE'])
          #print(param['TITLE_ID'])
          break


        input_iso.seek((core.SECTOR * counter))

        counter += 1

      game_title = ''

      if found_param:
        input_iso.seek(input_iso.tell() - 8)
        try:
          param = sfo.SFO(input_iso)
          core.vprint('PARAM.SFO found', args)

          game_title = core.multiman_title(param['TITLE'])

          if args.verbose and not args.quiet:
            param.print_info()

          # Set output to multiman style

          if not args.output:
            args.output = '%s [%s].iso' % (game_title, param['TITLE_ID'])

        except Exception:

          core.warning('Failed reading SFO', args)

    cipher = AES.new(core.ISO_SECRET, AES.MODE_CBC, core.ISO_IV)

    # TODO: clean up this logic

    if not args.decryption_key:
      if not args.ird:
        # No key or .ird specified. Let's first check if keys.db is packaged with this release

        redump = False

        core.vprint('Checking for bundled redump keys', args)

        try:
          try:
            db = sqlite3.connect(pkg_resources.resource_filename(__name__, 'data/keys.db'))
          except FileNotFoundError:
            db = sqlite3.connect((pathlib.Path(__file__).resolve() / 'data/') / 'keys.db')
          c = db.cursor()

          #core.vprint('Calculating crc32', args)

          #input_iso.seek(0)

          # crc32 = core.crc32(args.iso)

          #keys = c.execute('SELECT * FROM games WHERE crc32=?', [crc32.lower()]).fetchall()

          # First check if there's only one game with this exact size

          core.vprint('Trying to find redump key based on size', args)

          keys = c.execute('SELECT * FROM games WHERE size = ?', [str(self.size)]).fetchall()

          if len(keys) == 1:

            self.disc_key = keys[0][-1]

            redump = True

          # If not, see if we can filter it out based on name and size

          if not redump:

            core.vprint('Trying to find redump key based on size, game title, and country', args)

            if not game_title:
              raise ValueError

            keys = c.execute('SELECT * FROM games WHERE lower(name) LIKE ? AND size = ?', ['%' + '%'.join(game_title.lower().split(' ')) + '%' + core.serial_country(self.game_id).lower() + '%', str(self.size)]).fetchall()

            if keys:

              self.disc_key = keys[0][-1]

              redump = True

          if not self.disc_key:
            raise ValueError

          core.vprint('Found potential redump key: "%s"' % keys[0][0], args)

        except:
          core.vprint('No keys found', args)

        if not redump:

        # Fallback to checking if an .ird exists

          core.warning('No IRD file specified, finding required file', args)
          args.ird = core.ird_by_game_id(self.game_id) # Download ird

          self.ird = ird.IRD(args.ird)

          if self.ird.region_count != len(self.regions)-1:
            core.error('Corrupt ISO or error in IRD. Expected %s regions, found %s regions' % (self.ird.region_count, len(self.regions)-1))

          if self.regions[-1]['start'] > self.size:
            core.error('Corrupt ISO or error in IRD. Expected filesize larger than %.2f GiB, actual size is %.2f GiB' % (self.regions[-1]['start'] / 1024**3, self.size / 1024**3 ) )

          self.disc_key = cipher.encrypt(self.ird.data1)

      else:

        # .ird file given with -k / --ird

        self.ird = ird.IRD(args.ird)

        if self.ird.region_count != len(self.regions)-1:
          core.error('Corrupt ISO or error in IRD. Expected %s regions, found %s regions' % (self.ird.region_count, len(self.regions)-1))

        if self.regions[-1]['start'] > self.size:
          core.error('Corrupt ISO or error in IRD. Expected filesize larger than %.2f GiB, actual size is %.2f GiB' % (self.regions[-1]['start'] / 1024**3, self.size / 1024**3 ) )

        self.disc_key = cipher.encrypt(self.ird.data1)

    else:
      self.disc_key = core.to_bytes(args.decryption_key)

    if args.verbose and not args.quiet:
      self.print_info()


  def decrypt(self, args):
    """Decrypt self using args from argparse."""

    core.vprint('Decrypting with disc key: %s' % self.disc_key.hex(), args)

    with open(args.iso, 'rb') as input_iso:

      if not args.output:
        output_name = '%s.iso' % self.game_id
      else:
        output_name = args.output

      core.vprint('Decrypted .iso is output to: %s' % output_name, args)

      with open(output_name, 'wb') as output_iso:

        if not args.quiet:
          pbar = tqdm(total= (self.size // 2048) )

        for region in self.regions:
          input_iso.seek(region['start'])

          # Unencrypted region, just copy it
          if not region['enc']:
            while input_iso.tell() < region['end']:
              data = input_iso.read(core.SECTOR)
              if not data:
                core.warning('Trying to read past the end of the file', args)
                break
              output_iso.write(data)

              if not args.quiet:
                pbar.update(1)
            continue
          # Encrypted region, decrypt then write
          else:
            while input_iso.tell() < region['end']:
              num = input_iso.tell() // 2048
              iv = bytearray([0 for i in range(0,16)])
              for j in range(0,16):
                iv[16 - j - 1] = (num & 0xFF)
                num >>= 8

              data = input_iso.read(core.SECTOR)
              if not data:
                core.warning('Trying to read past the end of the file', args)
                break

              cipher = AES.new(self.disc_key, AES.MODE_CBC, bytes(iv))
              decrypted = cipher.decrypt(data)

              output_iso.write(decrypted)

              if not args.quiet:
                pbar.update(1)

        if not args.quiet:
          pbar.close()

        core.vprint('Decryption complete!', args)


  def encrypt(self, args):
    """Encrypt self using args from argparse."""

    core.vprint('Re-encrypting with disc key: %s' % self.disc_key.hex(), args)

    with open(args.iso, 'rb') as input_iso:

      if not args.output:
        output_name = '%s_e.iso' % self.game_id
      else:
        output_name = args.output

      core.vprint('Re-encrypted .iso is output to: %s' % output_name, args)

      with open(output_name, 'wb') as output_iso:

        if not args.quiet:
          pbar = tqdm(total= (self.size // 2048) )

        for region in self.regions:
          input_iso.seek(region['start'])

          # Unencrypted region, just copy it
          if not region['enc']:
            while input_iso.tell() < region['end']:
              data = input_iso.read(core.SECTOR)
              if not data:
                core.warning('Trying to read past the end of the file', args)
                break
              output_iso.write(data)

              if not args.quiet:
                pbar.update(1)
            continue
          # Decrypted region, re-encrypt it
          else:
            while input_iso.tell() < region['end']:
              num = input_iso.tell() // 2048
              iv = bytearray([0 for i in range(0,16)])
              for j in range(0,16):
                iv[16 - j - 1] = (num & 0xFF)
                num >>= 8

              data = input_iso.read(core.SECTOR)
              if not data:
                core.warning('Trying to read past the end of the file', args)
                break

              cipher = AES.new(self.disc_key, AES.MODE_CBC, bytes(iv))
              encrypted = cipher.encrypt(data)

              output_iso.write(encrypted)

              if not args.quiet:
                pbar.update(1)

        if not args.quiet:
          pbar.close()

        core.vprint('Re-encryption complete!', args)


  def print_info(self):
    # TODO: This could probably have been a __str__? Who cares?
    """Print some info about the ISO."""
    print('Game ID: %s' % self.game_id)
    print('Key: %s' % self.disc_key.hex())
    print('Info from ISO:')
    print('Regions: %s' % self.number_of_regions)
    for i, region in enumerate(self.regions):
      print(i, region)

