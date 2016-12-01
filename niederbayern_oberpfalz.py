# -*- coding: utf-8 -*-
#
#  niederbayern_oberpfalz.py
#
#  Copyright 2016 Alex Flierl <shad0w73@vmail.me>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

# TODO:
#   - find out new legend for "Aktionsgericht"

# Usable locations (urls) (based on http://www.stwno.de/joomla/de/gastronomie/speiseplan):
# HS-DEG - TH Deggendorf
# HS-LA - HS Landshut
# HS-SR - WZ Straubing
# Uni Passau:
#   UNI-P - Uni Passau
#   Cafeteria-Nikolakloster - Cafeteria Nikolakloster
# OTH Regensburg:
#   HS-R-tag - Seybothstraße (mittags)
#   HS-R-abend - Seybothstraße (abends)
#   Cafeteria-Pruefening - Prüfeningerstr. (mittags)
# Uni Regensburg:
#   UNI-R - Mensa (mittags)
#   Cafeteria-PT - Cafeteria PT (mittags)
#   Cafeteria-Chemie - Cafeteria Chemie
#   Cafeteria-Milchbar - Cafeteria Milchbar
#   Cafeteria-Sammelgebaeude - Cafeteria Sammelgebäude
#   Cafeteria-Sport - Cafeteria Sport

# header:
# 1 - datum
# 2 - tag
# 3 - warengruppe
# 4 - name
# 5 - kennz
# 6 - preis
# 7 - stud
# 8 - bed
# 9 - gast

import sys
from csv import reader
from datetime import date, timedelta
from urllib.request import urlopen
from urllib.error import HTTPError
import re

from utils import Parser

from pyopenmensa.feed import LazyBuilder


def parse_url(url, today=False):
    canteen = LazyBuilder()
    legend = {
        '1':     'mit Farbstoff',
        '2':     'mit Konservierungsstoff',
        '3':     'mit Antioxidationsmittel',
        '4':     'mit Geschmacksverstärker',
        '5':     'geschwefelt',
        '6':     'geschwärzt',
        '7':     'gewachst',
        '8':     'mit Phosphat',
        '9':     'mit Süssungsmittel Saccharin',
        '10':    'mit Süssungsmittel Aspartam, enth. Phenylalaninquelle',
        '11':    'mit Süssungsmittel Cyclamat',
        '12':    'mit Süssungsmittel Acesulfam',
        '13':    'chininhaltig',
        '14':    'coffeinhaltig',
        '15':    'gentechnisch verändert',
        '16':    'enthält Sulfite',
        '17':    'enthält Phenylalanin',
        'A':     'Gluten',
        'AA':    'Weizen',
        'AB':    'Roggen',
        'AC':    'Gerste',
        'AD':    'Hafer',
        'AE':    'Dinkel',
        'AF':    'Kamut',
        'B':     'Krebstiere',
        'C':     'Eier',
        'D':     'Fisch',
        'E':     'Erdnüsse',
        'F':     'Soja',
        'G':     'Milch und Milchprodukte',
        'H':     'Schalenfrüchte',
        'HA':    'Mandel',
        'HB':    'Haselnuss',
        'HC':    'Walnuss',
        'HD':    'Cashew',
        'HE':    'Pecannuss',
        'HF':    'Paranuss',
        'HG':    'Pistazie',
        'HH':    'Macadamianuss',
        'HI':    'Queenslandnuss',
        'I':     'Sellerie',
        'J':     'Senf',
        'K':     'Sesamsamen',
        'L':     'Schwefeldioxid und Sulfite',
        'M':     'Lupinen',
        'N':     'Weichtiere',
        'O':     'Nitrat',
        'P':     'Nitritpökelsalz',
        'ZTA':   'Alkohol',
        'ZTB':   'mit ausschließlich biologisch erzeugten Rohstoffen',
        'ZTF':   'Fisch',
        'ZTG':   'Geflügel',
        'ZTL':   'Lamm',
        'ZTMSC': 'zertifizierte nachhaltige Fischerei (MSC-C-53400)',
        'ZTMV':  'Mensa Vital',
        'ZTR':   'Rindfleisch',
        'ZTS':   'Schweinefleisch',
        'ZTV':   'vegetarisch',
        'ZTVG':  'vegan',
        'ZTW':   'Wild'
    }

    # Create regular expressions for categories
    hg = re.compile("^HG[1-9]$")
    b = re.compile("^B[1-9]$")
    n = re.compile("^N[1-9]$")

    # Get two weeks for full.xml and only the current one for today.xml
    # On error 404 continue with next isoweek
    # Returns an empty feed if both isoweeks result in error 404
    # At most locations the data doesn't exist on term break
    weeks = 1 if today else 2
    for w in range(0, weeks):
        kw = (date.today() + timedelta(weeks=w)).isocalendar()[1]
        try:
            f = urlopen('%(location)s/%(isoweek)d.csv' %
                        {'location': url, 'isoweek': kw})
        except HTTPError as e:
            if e.code == 404:
                continue
            else:
                raise e

        # Decode data from ISO charset
        f = f.read().decode('iso8859-1')

        # Set roles for prices
        roles = ('student', 'employee', 'other')

        # Read csv data and skip the csv header
        mealreader = reader(f.splitlines(), delimiter=';')
        next(mealreader)
        for row in mealreader:
            mdate = row[0]
            category = row[2]
            mname = row[3]
            mtype = row[4]
            prices = [row[6], row[7], row[8]]

            # determine category for the current meal
            if category == 'Suppe':
                pass
            elif hg.match(category):
                category = 'Hauptgerichte'
            elif b.match(category):
                category = 'Beilagen'
            elif n.match(category):
                category = 'Nachspeisen'
            else:
                raise RuntimeError('Unknown category: ' + str(category))

            # Extract the notes from brackets in the meal name
            # Remove the brackets, notes and improve readability
            notes = []
            bpos = mname.find(')')
            while bpos != -1:
                apos = mname.find('(')
                # Extract notes from current brackets and avoid empty notes
                for i in mname[apos+1:bpos].split(','):
                    if i:
                        notes.append(i)
                # Check if brackets are at the end of the meal name
                if bpos == len(mname)-1:
                    # Remove brackets and break bracket loop
                    mname = mname[:apos]
                    bpos = -1
                else:
                    # Remove current brackets, improve readability
                    # and find the next brackets
                    mname = mname[:apos].rstrip() + ' und ' + mname[bpos+1:].lstrip()
                    bpos = mname.find(')')

            # Remove trailing whitespaces in the meal name
            mname = mname.rstrip()

            # Add meal type notes to notes list and avoid empty notes
            for i in mtype.split(','):
                if i:
                    notes.append('ZT' + i)

            # Translate notes via legend to human readable information
            mnotes = []
            for i in notes:
                mnotes.append(legend.get(i, legend.get(i[2:], i)))

            # Try to add the meal
            try:
                canteen.addMeal( mdate, category, mname,
                                mnotes, prices, roles)
            except ValueError as e:
                print('could not add meal {}/{} "{}" due to "{}"'.format(mdate, category, mname, e), file=sys.stderr)
                # empty meal ...
                pass

    # return xml data
    return canteen.toXMLFeed()


parser = Parser('niederbayern_oberpfalz', handler=parse_url,
                shared_prefix='http://www.stwno.de/infomax/daten-extern/csv/')
parser.define('th-deggendorf', suffix='HS-DEG')
parser.define('hs-landshut', suffix='HS-LA')
parser.define('wz-straubing', suffix='HS-SR')
parser.define('uni-passau', suffix='UNI-P')
parser.define('unip-cafeteria-nikolakloster', suffix='Cafeteria-Nikolakloster')
parser.define('oth-regensburg', suffix='HS-R-tag')
parser.define('oth-regensburg-abends', suffix='HS-R-abend')
parser.define('othr-cafeteria-pruefening', suffix='Cafeteria-Pruefening')
parser.define('uni-regensburg', suffix='UNI-R')
parser.define('unir-cafeteria-pt', suffix='Cafeteria-PT')
parser.define('unir-cafeteria-chemie', suffix='Cafeteria-Chemie')
parser.define('unir-cafeteria-milchbar', suffix='Cafeteria-Milchbar')
parser.define('unir-cafeteria-sammelgebaeude', suffix='Cafeteria-Sammelgebaeude')
parser.define('unir-cafeteria-sport', suffix='Cafeteria-Sport')
