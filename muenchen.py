#!python3
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as parse
import re
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')
otherPrice = re.compile('Gästezuschlag:? ?(?P<price>\d+[,.]\d{2}) ?€?')

base = 'http://www.studentenwerk-muenchen.de/mensa'


def parse_url(url, today=False):
    canteen = LazyBuilder()
    legend = {'f': 'fleischloses Gericht', 'v': 'veganes Gericht'}
    document = parse(urlopen(base + '/speiseplan/zusatzstoffe-de.html').read())
    for td in document.find_all('td', 'beschreibung'):
        legend[td.previous_sibling.previous_sibling.text] = td.text
    document = parse(urlopen(base + '/unsere-preise/').read())
    prices = {}
    for tr in document.find('table', 'essenspreise').find_all('tr'):
        meal = tr.find('th')
        if not meal or not meal.text.strip():
            continue
        if len(tr.find_all('td', 'betrag')) < 3:
            continue
        if 'titel' in meal.attrs.get('class', []) or 'zeilentitel' in meal.attrs.get('class', []):
            continue
        meal = meal.text.strip()
        prices[meal] = {}
        for role, _id in [('student', 0), ('employee', 1), ('other', 2)]:
            price_html = tr.find_all('td', 'betrag')[_id].text
            price_search = price_regex.search(price_html)
            if price_search:
                prices[meal][role] = price_search.group('price')
    errorCount = 0
    date = datetime.date.today()
    while errorCount < 7:
        try:
            document = parse(urlopen(url.format(date)).read())
        except HTTPError as e:
            if e.code == 404:
                errorCount += 1
                date += datetime.date.resolution
                continue
            else:
                raise e
        else:
            errorCount = 0
        for tr in document.find('table', 'zusatzstoffe').find_all('tr'):
            identifier = tr.find_all('td')[0].text \
                           .replace('(', '').replace(')', '')
            legend[identifier] = tr.find_all('td')[1].text.strip()
        canteen.setLegendData(legend)
        mensa_data = document.find('table', 'menu')
        category = None
        for menu_tr in mensa_data.find_all('tr'):
            if menu_tr.find('td', 'headline'):
                continue
            if menu_tr.find('td', 'gericht').text:
                category = menu_tr.find('td', 'gericht').text
            data = menu_tr.find('td', 'beschreibung')
            name = data.find('span').text.strip()
            notes = [span['title'] for span in data.find_all('span', title=True)]
            canteen.addMeal(
                date, category, name, notes,
                prices.get(category.replace('Aktionsessen', 'Bio-/Aktionsgericht'), {})
            )
        date += datetime.date.resolution
        if today:
            break
    return canteen.toXMLFeed()


parser = Parser('muenchen', handler=parse_url,
                shared_prefix='http://www.studentenwerk-muenchen.de/mensa/speiseplan/')
parser.define('leopoldstrasse', suffix='speiseplan_{}_411_-de.html')
parser.define('martinsried', suffix='speiseplan_{}_412_-de.html')
parser.define('grosshadern', suffix='speiseplan_{}_414_-de.html')
parser.define('schellingstrasse', suffix='speiseplan_{}_416_-de.html')
parser.define('archisstrasse', suffix='speiseplan_{}_421_-de.html')
parser.define('garching', suffix='speiseplan_{}_422_-de.html')
parser.define('weihenstephan', suffix='speiseplan_{}_423_-de.html')
parser.define('lothstrasse', suffix='speiseplan_{}_431_-de.html')
parser.define('pasing', suffix='speiseplan_{}_432_-de.html')
parser.define('rosenheim', suffix='speiseplan_{}_441_-de.html')
parser.define('adalbertstrasse', suffix='speiseplan_{}_512_-de.html')
parser.define('cafeteria-garching', suffix='speiseplan_{}_524_-de.html')
parser.define('wst', suffix='speiseplan_{}_525_-de.html')
parser.define('akademie', suffix='speiseplan_{}_526_-de.html')
parser.define('boltzmannstrasse', suffix='speiseplan_{}_527_-de.html')
parser.define('karlstrasse', suffix='speiseplan_{}_532_-de.html')
