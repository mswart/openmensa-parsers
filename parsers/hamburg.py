from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from datetime import date

from utils import Parser

from pyopenmensa.feed import LazyBuilder, extractWeekDates

extra_regex = re.compile('\(.*?\)')
strip_regex = re.compile('\s{2,}')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')


def parse_week(url, date, canteen):
    url += '/{0}/{1:0>2}/'.format(*date.isocalendar())
    document = parse(urlopen(url).read())
    week_data = document.find('table', id='week-menu')
    if week_data is None:
        print('week not found')
        return
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


def parse_url(url, today=False):
    canteen = LazyBuilder()
    parse_week(url, date.today(), canteen)
    if not today:
        parse_week(url, date.today() + date.resolution * 7, canteen)
    return canteen.toXMLFeed()


parser = Parser('hamburg', handler=parse_url,
                shared_prefix='http://speiseplan.studierendenwerk-hamburg.de/de/')
parser.define('armgartstrasse', suffix='590')
parser.define('bergedorf', suffix='520')
parser.define('berliner-tor', suffix='530')
parser.define('botanischer-garten', suffix='560')
parser.define('bucerius-law-school', suffix='410')
parser.define('cafe-mittelweg', suffix='690')
parser.define('cafe-cfel', suffix='680')
parser.define('cafe-jungiusstrasse', suffix='610')
parser.define('cafe-alexanderstrasse', suffix='660')
parser.define('campus', suffix='340')
parser.define('finkenau', suffix='420')
parser.define('geomatikum', suffix='540')
parser.define('harburg', suffix='570')
parser.define('hcu', suffix='430')
parser.define('philosophenturm', suffix='350')
parser.define('stellingen', suffix='580')
parser.define('studierendenhaus', suffix='310')
