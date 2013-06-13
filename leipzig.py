#!python3
from urllib.request import urlopen
import json
import datetime

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
    while emptyCount < 7:
        print(canteen._days)
        if not parse_day(canteen, '{}&day={}&month={}&year={}&limit=25'
                         .format(url, day.day, day.month, day.year),
                         day.strftime('%Y-%m-%d')):
            emptyCount += 1
        else:
            emptyCount = 0
        if today:
            break
        day += datetime.date.resolution
    return canteen.toXMLFeed()
