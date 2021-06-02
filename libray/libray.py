#!/usr/bin/env python3
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


import argparse


try:
  from libray import core
except ImportError:
  import core


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='A Libre (FLOSS) Python application for unencrypting, extracting, repackaging, and encrypting PS3 ISOs')
  parser._action_groups.pop()

  required = parser.add_argument_group('required arguments')
  required.add_argument('-i', '--iso', dest='iso', type=str, help='Path to .iso file or stream', required=True)

  optional = parser.add_argument_group('optional arguments')
  optional.add_argument('-o', '--output', dest='output', type=str, help='Output filename', default='')
  optional.add_argument('-k', '--ird', dest='ird', type=str, help='Path to .ird file', default='')
  optional.add_argument('-d', '--decryption-key', dest='decryption_key', type=str, help='Manually specify key', default='')
  optional.add_argument('-v', '--verbose', dest='verbose', help='Increase verbosity', action='count')
  optional.add_argument('-q', '--quiet', dest='quiet', help='Quiet mode, only prints on error', action='store_true')
  # -e is reserved for "extract" so re-encrypt is "-r"
  optional.add_argument('-r', '--re-encrypt', dest='reencrypt', help='Re-encrypt .iso', action='store_true')

  args = parser.parse_args()

  if args.reencrypt:

    core.encrypt(args)

  else:

    core.decrypt(args)
