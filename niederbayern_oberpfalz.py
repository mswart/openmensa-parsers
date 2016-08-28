#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  niederbayern_oberpfalz.py
#
#  Copyright 2015 shad0w73 <shad0w73@vmail.me>
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
# - update usable locations
# - comment the code

# Usable locations (urls) (based on http://www.stwno.de/joomla/de/gastronomie/speiseplan):
# HS-DEG - TH Deggendorf
# HS-LA - HS Landshut
# UNI-P - Uni Passau
# OTH Regensburg:
#   HS-R-tag - Seybothstraße (mittags)
#   HS-R-abend - Seybothstraße (abends) (currently no data)
#   Cafeteria-Pruefening - Prüfeningerstr. (mittags) (currently no data)
# Uni Regensburg:
#   UNI-R - Mensa (mittags)
#   Cafeteria-PT - Cafeteria PT (mittags) (currently no data)
#   Cafeteria-Chemie - Cafeteria Chemie (currently no data)
#   Cafeteria-Milchbar - Cafeteria Milchbar (currently no data)
#   Cafeteria-Sammelgebaeude - Cafeteria Sammelgebäude (currently no data)
#   Cafeteria-Sport - Cafeteria Sport (currently no data)

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
        'B':     'Krebstiere',
        'C':     'Eier',
        'D':     'Fisch',
        'E':     'Erdnüsse',
        'F':     'Soja',
        'G':     'Milch und Milchprodukte',
        'H':     'Schalenfrüchte',
        'I':     'Sellerie',
        'J':     'Senf',
        'K':     'Sesamsamen',
        'L':     'Schwefeldioxid und Sulfite',
        'M':     'Lupinen',
        'N':     'Weichtiere',
        'ZTA':   'Aktionsgericht',
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
    #canteen.setLegendData(legend)

    hg = re.compile("^HG[1-9]$")
    b = re.compile("^B[1-9]$")
    n = re.compile("^N[1-9]$")

    #for w in 0, 1:
    for w in [0]:
        kw = (date.today() + timedelta(weeks=w)).isocalendar()[1]
        try:
            f = urlopen('%(location)s/%(isoweek)d.csv' %
                        {'location': url, 'isoweek': kw})
        except HTTPError as e:
            if e.code == 404:
                continue
            else:
                raise e
        f = f.read().decode('iso8859-1')

        roles = ('student', 'employee', 'other')

        initline = True
        mealreader = reader(f.splitlines(), delimiter=';')
        for row in mealreader:
            if initline:
                initline = False
            else:
                if row[2] == 'Suppe':
                    category = 'Suppe'
                elif hg.match(row[2]):
                    category = 'Hauptgerichte'
                elif b.match(row[2]):
                    category = 'Beilagen'
                elif n.match(row[2]):
                    category = 'Nachspeisen'
                else:
                    raise RuntimeError('Unknown category: ' + str(row[2]))

                mdate = row[0]
                notes = []

                mname = row[3]
                bpos = mname.find(')')
                while bpos != -1:
                    apos = mname.find('(')
                    for i in mname[apos+1:bpos].split(','):
                        if i:
                            notes.append(i)
                    if bpos == len(mname)-1:
                        mname = mname[:apos] + mname[bpos+1:]
                        bpos = -1
                    else:
                        mname = mname[:apos] + ' und ' + mname[bpos+1:]
                        bpos = mname.find(')')
                if mname.rfind(' ') == len(mname)-1:
                    mname = mname[:len(mname)-1]

                mtype = row[4]
                if mtype != '':
                    for i in mtype.split(','):
                        if i:
                            notes.append('ZT' + i)

                prices = [row[6], row[7], row[8]]

                mnotes = []
                for i in notes:
                    mnotes.append(legend.get(i, legend.get(i[2:], i)))

                try:
                    canteen.addMeal(mdate, category, mname,
                                    mnotes, prices, roles)
                except ValueError as e:
                    print('could not add meal {}/{} "{}" due to "{}"'.format(mdate, category, mname, e), file=sys.stderr)
                    # empty meal ...
                    pass

    return canteen.toXMLFeed()


parser = Parser('niederbayern_oberpfalz', handler=parse_url,
                shared_prefix='http://www.stwno.de/infomax/daten-extern/csv/')
parser.define('th-deggendorf', suffix='HS-DEG')
parser.define('hs-landshut', suffix='HS-LA')
parser.define('uni-passau', suffix='UNI-P')
parser.define('oth-regensburg', suffix='HS-R-tag')
parser.define('uni-regensburg', suffix='UNI-R')
