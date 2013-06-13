#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{4}-\d{2}-\d{2})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')

roles = ('student', 'other', 'employee', 'pupil')


def parse_week(canteen, url, place_class=None):
    content = urlopen(url).read()
    document = parse(content)
    legends = document.find_all('div', {'class': 'legende'})
    if len(legends) > 0:
        extraLegend = {int(v[0]): v[1] for v in reversed(legend_regex.findall(legends[0].text))}
    else:
        extraLegend = {}

    if place_class:
        document = document.find(id=place_class)

    for day_a in document.find_all('a', rel=day_regex):
        day_data = document.find(id=day_a['href'].replace('#', ''))
        if not day_data:
            continue
        date = day_a['rel'][0]
        day_table = day_data.table
        if not day_table:
            continue
        if day_table.tbody:
            day_table = day_table.tbody
        canteen.clearDay(date)  # remove old data about this day
        for category_tr in day_table.children:
            if category_tr.name != 'tr':
                continue
            if len(category_tr) < 2:
                continue  # no meal
            category = category_tr.contents[0].text
            meal_table = category_tr.contents[1].table
            if meal_table.tbody:
                meal_table = meal_table.tbody
            for meal_tr in meal_table.children:
                if meal_tr.name != 'tr':
                    continue
                if len(list(meal_tr.children)) != 3:
                    #print('skipping category, unable to parse meal_table: {} tds'.format(len(list(meal_tr.children))))
                    continue
                name = meal_tr.contents[1].text
                # notes, to do
                canteen.addMeal(date, category, name, [],
                                price_regex.findall(meal_tr.contents[2].text), roles)


def parse_url(url, today=False, place_class=None):
    canteen = OpenMensaCanteen()
    parse_week(canteen, url, place_class)
    day = datetime.date.today()
    old = -1
    day += datetime.date.resolution * 7
    if not today:
        parse_week(canteen, '{}?kw={}'.format(url, day.isocalendar()[1]), place_class)
    day += datetime.date.resolution * 7
    while not today and old != canteen.dayCount():
        old = canteen.dayCount()
        parse_week(canteen, '{}?kw={}'.format(url, day.isocalendar()[1]), place_class)
        day += datetime.date.resolution * 7
    return canteen.toXMLFeed()
