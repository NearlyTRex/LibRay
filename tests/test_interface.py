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

# This is a script to find the redump names and game serial id's using rpcs3's compatibility list.
# It puts the name, serial id, and some other info into an sqlite3 database.
# That database can then be used to harcode serial id to keys into keys.db.
# This script is not included in the release of libray.


import io
import argparse
import builtins
import unittest
import unittest.mock

import libray


class TestInterface(unittest.TestCase):



    @unittest.mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace())
    def test_decrypt_with_key(self, mock_args):

        io_object = io.BytesIO(b"some initial binary data: \x00\x01")

        os_stat = unittest.mock.Mock()
        os_stat.return_value.st_mode = 33188

        iso_filepath = unittest.mock.Mock()
        iso_filepath.open = unittest.mock.mock_open(read_data=b"some initial binary data: \x00\x01")

        iso_filepath.is_file.return_value = True
        iso_filepath.stat.return_value = unittest.mock.MagicMock()
        iso_filepath.stat.st_size = 1024
        iso_filepath.stat.st_mode = 33188
        iso_filepath.stat.S_ISBLK.return_value = False

        mock_args.iso = 'encrypted_mock.iso'

        #mock_args.iso = iso_filepath

        with unittest.mock.patch('os.stat', os_stat):

            with unittest.mock.patch('builtins.open', iso_filepath.open):

                libray.core.decrypt(mock_args)



