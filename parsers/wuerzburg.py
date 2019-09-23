from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

day_regex = re.compile('(?P<day>\d{2})\.(?P<month>\d{2})\.')
price_map = {
    'default': 'student',
    'bed': 'employee',
    'guest': 'other',
}

def parse_url(url, today=False):
    canteen = LazyBuilder()
    document = parse(urlopen(url).read(), 'lxml')

    for day_div in document.find_all('div', attrs={'data-day': True}):
        # parse date, warning: calculate year number needed
        date_test = day_regex.search(day_div['data-day'])
        if not date_test:
            print('Error: unable to parse date "{}"'.format(day_div['data-day']))
            continue
        else:
            year = datetime.datetime.now().year
            if datetime.datetime.now().month > int(date_test.group('month')):
                year += 1  # date from next year
            date = '{}-{}-{}'.format(year, date_test.group('month'), date_test.group('day'))

        closed_candidate = day_div.find('div', 'holiday') is not None

        for meal_article in day_div.find_all('article', 'menu'):
            name = meal_article.find('div', 'title').text
            if not name:
                continue

            category = meal_article.find('div', 'icon')['title']
            notes = []
            prices = {}

            additives = meal_article.find('div', 'additnr')
            if additives:
                notes += [additive.text for additive in additives.find_all('li')]
            notes += [v['title'] for v in meal_article.find_all('div', 'theicon') if v['title'] and v['title'] not in notes]

            price_div = meal_article.find('div', 'price')
            if price_div:
                for k, v in price_map.items():
                    price = price_div['data-' + k]
                    if price:
                        prices[v] = price
            canteen.addMeal(date, category, name, notes, prices)

        if closed_candidate and not canteen.hasMealsFor(date):
            canteen.setDayClosed(date)

    return canteen.toXMLFeed()


parser = Parser('wuerzburg', handler=parse_url,
                shared_prefix='https://www.studentenwerk-wuerzburg.de/essen-trinken/speiseplaene/')
#parser.define('austrasse', suffix='austrasse-bamberg.html')
parser.define('markusplatz', suffix='interimsmensa-markusplatz-bamberg.html')
parser.define('burse', suffix='burse-am-studentenhaus-wuerzburg.html')
parser.define('feldkirchenstrasse', suffix='feldkirchenstrasse-bamberg.html')
#parser.define('frankenstube', suffix='frankenstube-wuerzburg.html')
#parser.define('hubland', suffix='mensa-am-hubland-wuerzburg.html')
parser.define('studentenhaus', suffix='mensa-am-studentenhaus.html')
parser.define('aschaffenburg', suffix='mensa-aschaffenburg.html')
parser.define('augenklinik', suffix='mensa-roentgenring-wuerzburg.html')
parser.define('josef-schneider', suffix='mensa-josef-schneider-strasse-wuerzburg.html')
parser.define('schweinfurt', suffix='mensa-schweinfurt.html')
parser.define('mensateria', suffix='mensateria-campus-hubland-nord-wuerzburg.html')
parser.define('philo', suffix='essensausgabe-philo-wuerzburg.html')
parser.define('sprachenzentrum', suffix='interimsmensa-im-sprachenzentrum-ab-9-april-2018.html')
