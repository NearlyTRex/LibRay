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

# This is a script to find the redump names and game serial id's using rpcs3's compatibility list.
# It puts the name, serial id, and some other info into an sqlite3 database.
# That database can then be used to harcode serial id to keys into keys.db.
# This script is not included in the release of libray.


import bs4
import string
import sqlite3
import pathlib
import requests


if __name__ == '__main__':

    db_path = pathlib.Path('games.db')

    #if db_path.exists():
    #    db_path.unlink()

    db = sqlite3.connect(db_path)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS games (serial TEXT PRIMARY KEY, country TEXT, type TEXT, name TEXT, redump_name TEXT)')
    db.commit()

    # "#" section

    for i in range(1, 18):

        url = 'https://rpcs3.net/compatibility?r=200&p=' + str(i)

        print('Requesting page ' + str(i))

        response = requests.get(url)

        soup = bs4.BeautifulSoup(response.text, features='html5lib')

        for row in soup.find_all('label', attrs={'class': 'compat-table-row'}):

            columns = [column for column in row.find_all('div', attrs={'class': 'compat-table-cell'})]

            for serial in columns[0].find_all(['img']):

                game_id = serial.attrs['title'].strip()
                country = serial.attrs['src'].split('/')[-1].split('.')[0]
                game_type = columns[1].find('a').attrs['title'].strip()
                name = columns[1].text.strip()

                redump_name = ''

                entry = [
                    game_id,
                    country,
                    game_type,
                    name,
                    country,
                    game_type,
                    name
                ]

                c.execute('INSERT INTO games VALUES (?, ?, ?, ?, ?) ON CONFLICT DO UPDATE SET country = ?, type = ?, name = ? ', entry)

        db.commit()





