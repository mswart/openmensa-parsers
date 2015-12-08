#!python3
from urllib.request import urlopen
import json
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder


def correct_prices(v):
    if 'employe' in v:
        v['employee'] = v.pop('employe')
    if 'guest' in v:
        v['other'] = v.pop('guest')
    return v


def parse_day(canteen, url, date):
    content = urlopen(url).read()
    data = json.loads(content.decode('utf-8'))

    for category in data:
        for meal in category['components']:
            notes = filter(lambda v: v, map(lambda v: v.strip(),
                           category['ingredients'].split(',') +
                           category['additives'].split(',')))
            if type(meal) is str:
                canteen.addMeal(date, category['name'], meal, notes,
                                correct_prices(category['prices']))
            elif type(meal) is dict:
                canteen.addMeal(date, category['name'], meal['name'], notes,
                                correct_prices(meal['prices']))
            else:
                print('unknown meal type: {}'.format(type(meal)))
    return len(data) > 0


def parse_url(url, today=False):
    canteen = LazyBuilder()
    day = datetime.date.today()
    emptyCount = 0
    totalCount = 0
    while emptyCount < 7 and totalCount < 32:
        if not parse_day(canteen, '{}&day={}&month={}&year={}&limit=25'
                         .format(url, day.day, day.month, day.year),
                         day.strftime('%Y-%m-%d')):
            emptyCount += 1
        else:
            emptyCount = 0
        if today:
            break
        totalCount += 1
        day += datetime.date.resolution
    return canteen.toXMLFeed()


parser = Parser('leipzig', handler=parse_url,
                shared_prefix='http://www.studentenwerk-leipzig.de/mensen-und-cafeterien/speiseplan/m/meals.php?canteen=')
parser.define('dittrichring', suffix='153')
parser.define('koburger-strasse', suffix='121')
parser.define('philipp-rosenthal-strasse', suffix='127')
parser.define('waechterstrasse', suffix='129')
parser.define('academica', suffix='118')
parser.define('am-park', suffix='106')
parser.define('am-elsterbecken', suffix='115')
parser.define('liebigstrasse', suffix='162')
parser.define('peterssteinweg', suffix='111')
parser.define('schoenauer-strasse', suffix='140')
parser.define('tierklinik', suffix='170')
