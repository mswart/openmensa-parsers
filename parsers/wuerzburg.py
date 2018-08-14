from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

day_regex = re.compile('(?P<day>\d{2})\.(?P<month>\d{2})\.')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
extra_regex = re.compile('[0-9,]+=(?P<note>\w+(\s|\w)*)')


def parse_url(url, today=False):
    canteen = LazyBuilder()
    document = parse(urlopen(url).read())
    for day_div in document.find_all('div', 'day') + document.find_all('article', attrs={'data-day': True}):
        # parse date, warning: calculate year number needed
        date_test = day_regex.search(day_div['data-day'])
        if not date_test:
            print('Error: unable to parse date')
            continue
        else:
            year = datetime.datetime.now().year
            if datetime.datetime.now().month > int(date_test.group('month')):
                year += 1  # date from next year
            date = "{}-{}-{}".format(year, date_test.group('month'), date_test.group('day'), )
        if 'nodata' in day_div.attrs.get('class', []) or 'GESCHLOSSEN' in day_div.text:
            canteen.setDayClosed(date)
            continue
        closed_candidate = False
        for meal_article in day_div.find_all('article', 'menu'):
            name = meal_article.find('div', 'title').text
            if not name:
                continue
            if 'geschlossen' in name:
                closed_candidate = True
                continue
            category = meal_article.find('div')['title']
            notes = [v['title'] for v in meal_article.find_all('div', 'theicon') if v['title']]
            if meal_article.find('div', 'additive'):
                notes += [v[0] for v in extra_regex.findall(meal_article.find('div', 'additive').text)]
            price_div = meal_article.find('div', 'price')
            if price_div is None:
                canteen.addMeal(date, category, name, notes)
                continue
            prices = {}
            for v, r in (('default', 'student'), ('bed', 'employee'), ('guest', 'other')):
                price = price_regex.search(price_div['data-' + v])
                if price:
                    prices[r] = price.group('price')
                elif v == 'default':
                    prices = {}
                    break
            canteen.addMeal(date, category, name, notes, prices)
        if closed_candidate and not canteen.hasMealsFor(date):
            canteen.setDayClosed(date)
    return canteen.toXMLFeed()


parser = Parser('wuerzburg', handler=parse_url,
                shared_prefix='https://www.studentenwerk-wuerzburg.de/essen-trinken/speiseplaene/plan/')
parser.define('austrasse', suffix='austrasse-bamberg.html')
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
parser.define('philo', suffix='philosophie-wuerzburg.html')
parser.define('sprachenzentrum', suffix='interimsmensa-im-sprachenzentrum-ab-9-april-2018.html')