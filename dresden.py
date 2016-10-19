from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re

from utils import Parser

from pyopenmensa.feed import LazyBuilder, extractDate

price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')

roles = ('student', 'employee')


def parse_week(url, canteen):
    document = parse(urlopen(url).read())
    for day_table in document.find_all('table', 'speiseplan'):
        date = extractDate(day_table.thead.tr.th.text)
        if day_table.find('td', 'keinangebot'):
            canteen.setDayClosed(date)
            continue
        for meal_tr in day_table.tbody.children:
            if len(meal_tr.find_all('a') or []) < 1:
                continue
            name = meal_tr.td.text
            if ': ' in name:
                category, name = name.split(': ', 1)
            else:
                category = 'Angebote'
            if len(name) > 200:
                name = name[:200] + ' ...'
            notes = []
            for img in meal_tr.contents[1].find_all('img'):
                notes.append(img['title'])
            canteen.addMeal(date, category, name, notes,
                            price_regex.findall(meal_tr.contents[2].text), roles)


def parse_url(url, today=False):
    canteen = LazyBuilder()
    parse_week(url + '.html', canteen)
    if not today:
        parse_week(url + '-w1.html', canteen)
        parse_week(url + '-w2.html', canteen)
    return canteen.toXMLFeed()


parser = Parser('dresden', handler=parse_url,
                shared_prefix='http://www.studentenwerk-dresden.de/mensen/speiseplan/')
parser.define('reichenbachstrasse', suffix='mensa-reichenbachstrasse')
parser.define('zeltschloesschen', suffix='zeltschloesschen')
parser.define('alte-mensa', suffix='alte-mensa')
parser.define('mensologie', suffix='mensologie')
parser.define('siedepunkt', suffix='mensa-siedepunkt')
parser.define('johannstadt', suffix='mensa-johannstadt')
parser.define('wueins', suffix='mensa-wueins')
parser.define('bruehl', suffix='mensa-bruehl')
parser.define('u-boot', suffix='u-boot')
parser.define('tellerrandt', suffix='mensa-tellerrandt')
parser.define('zittau', suffix='mensa-zittau')
parser.define('stimm-gabel', suffix='mensa-stimm-gabel')
parser.define('palucca-schule', suffix='mensa-palucca-schule')
parser.define('goerlitz', suffix='mensa-goerlitz')
parser.define('sport', suffix='mensa-sport')
parser.define('kreuzgymnasium', suffix='mensa-kreuzgymnasium')
