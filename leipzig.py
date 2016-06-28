#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

def parse_prices(prices):
    price_map = {}
    for price in prices:
        id = price.get('consumerID')
        if '0' == id:
            price_map['student'] = price.getText()
        elif '1' == id:
            price_map['employee'] = price.getText()
        elif '2' == id:
            price_map['other'] = price.getText()
    return price_map

def parse_day(canteen, url):
    content = urlopen(url).read()
    data = BeautifulSoup(content.decode('utf-8'), 'xml')

    for group in data.findChildren('group'):
        date = group['productiondate']
        category = group.findChild('name').getText()
        prices = parse_prices(group.findChild('prices').findChildren('price'))

        components = group.findChild('components').findChildren('component')
        components = [ c.findChild("name1").getText() for c in components ]

        tags = group.findChild('taggings').findChildren('tagging')
        tags = [ t.getText() for t in tags if not t.is_empty_element ]

        if '1' == group['type']:
            # meal consisting of multiple parts, use first component as name

            if len(components) < 1:
                print("meal without component: {}".format(group))
                continue

            notes = components[1:] + tags
            canteen.addMeal(date, category, components[0], notes, prices)
        elif '2' == group['type']:
            # multiple components to choose from

            for component in components:
                canteen.addMeal(date, category, component, tags, prices)
        else:
            print('unknown meal type: {}'.format(group['type']))


def parse_url(url, today=False):
    canteen = LazyBuilder()
    day = datetime.date.today()
    for _ in range(21):
        parse_day(canteen, '{}&date={}'.format(url, day.strftime('%Y-%m-%d')))
        if today:
            break
        day += datetime.timedelta(days=1)
    return canteen.toXMLFeed()


parser = Parser('leipzig', handler=parse_url,
                shared_prefix='https://www.studentenwerk-leipzig.de/XMLInterface/request?location=')
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
