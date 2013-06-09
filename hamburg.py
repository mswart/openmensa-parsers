#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import LazyBuilder, extractWeekDates

extra_regex = re.compile('\(.*?\)')
strip_regex = re.compile('\s{2,}')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')


def parse_week(url, canteen):
    document = parse(urlopen(url).read())
    week_data = document.find('table', id='week-menu')
    weekDays = extractWeekDates(week_data.thead.find_all('th')[0].text)
    for category_tr in week_data.find_all('tr'):
        category = category_tr.find('th').text
        i = 0
        for day_td in category_tr.find_all('td'):
            for meal_data in day_td.find_all('p', 'dish'):
                if not meal_data.find('strong'):
                    continue
                name = extra_regex.sub('', meal_data.find('strong').text)
                name = strip_regex.sub(' ', name).strip()
                if len(name) > 250:
                    name = name[:245] + '...'
                notes = [span['title'] for span in meal_data.find_all('span', 'tooltip')]
                notes += [img['title'] for img in meal_data.find_all('img')]
                prices = price_regex.findall(meal_data.find('span', 'price').text)
                canteen.addMeal(weekDays[i], category, name,
                                list(set(notes)),
                                prices, ('student', 'employee', 'other')
                                )
            i += 1


def parse_url(url):
    canteen = LazyBuilder()
    parse_week(url + (datetime.date.today()
               + datetime.date.resolution * 7).strftime('/%Y/%W/'), canteen)
    parse_week(url + (datetime.date.today()
               + datetime.date.resolution * 14).strftime('/%Y/%W/'), canteen)
    return canteen.toXMLFeed()
