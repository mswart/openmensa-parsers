#!python3
from urllib.request import urlopen
import re
from xml.dom.minidom import Document

from pyopenmensa.feed import LazyBuilder

day_regex = re.compile('(?P<date>\d{2}\.\d{2}\.\d{4})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2})€')
note_regex = re.compile('\((?P<number>[a-z0-9]+?)\)')
legend_regex = re.compile('\((?P<number>\w+)\) ?(?P<value>\w+(\s+\w+)*)')
meal_regex = re.compile('(?P<category>(\w|\s|\(|\))+):\s*(?P<meal>[^0-9\(]+)')

roles = ('student', 'employee', 'other')


def parse_week(url, canteen):
    document = urlopen(url).read().decode('utf8').split('\n')
    legends = {v.group('number'): v.group('value') for v in map(lambda v: legend_regex.match(v), document) if v}
    date = None
    for line in document:
        if not date:
            test = day_regex.search(line)
            if test:
                date = test.group('date')
            continue
        if 'geschlossen' in line.lower():
            canteen.setDayClosed(date)
        if not line.startswith('>'):
            date = None
            continue
        mealtest = meal_regex.search(line)
        if not mealtest:
            print('unable to parse category/meal: "{}"'.format(line))
            continue
        category = mealtest.group('category').strip()
        name = mealtest.group('meal').strip()
        notes = []
        for notematch in note_regex.findall(line):
            if notematch not in legends:
                print('unknown legend: {}'.format(notematch))
                continue
            notes.append(legends[notematch])
        canteen.addMeal(date, category, name, notes,
                        price_regex.findall(line), roles)


def parse_url(url, today=False):
    canteen = LazyBuilder()
    parse_week(url + '&wann=2', canteen)
    if not today:
        parse_week(url + '&wann=3', canteen)
    return canteen.toXMLFeed()
