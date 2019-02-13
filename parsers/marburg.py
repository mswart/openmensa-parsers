from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re

from utils import Parser

from pyopenmensa.feed import LazyBuilder, extractDate

notes_regex = re.compile(r'\((\d+,?\s*)*\)\s*')
price_regex = re.compile(r'(?P<price>\d+[,.]\d{2}) ?€')
whitspace_regex = re.compile(r'\s+')
comma_regex = re.compile(r'\s*,\s*')
bracket_regex = re.compile(r'\s*\(\s*')

roles = ('student',)


def parse_dish(dish, canteen):

    date = extractDate(dish['data-date'])

    name = dish.find(class_='neo-menu-single-title')
    if name is not None:
        notes = set(x['title'] for x in name.find_all(name='abbr'))
    else:
        return

    name = re.sub(notes_regex, '', name.text.strip())
    if len(name) == 0:
        return

    # Fix formating issues:
    name = re.sub(whitspace_regex, ' ', name)  # Multiple Whitespace
    name = re.sub(comma_regex, ', ', name.strip(', '))  # No whitspace after comma
    name = re.sub(bracket_regex, ' (', name)

    category = dish.find(class_='neo-menu-single-type')
    if category is not None:
        category = category.text
    elif dish.find_previous(name='h2') is not None:
        # A side
        category = 'Beilagen: ' + dish.find_previous(name='h2').text.capitalize()
    else:
        # Just in case
        category = 'Unbekannt'

    price = dish.find(class_='neo-menu-single-price')
    if price is not None:
        prices = price_regex.findall(price.text)
    else:
        prices = {}

    canteen.addMeal(date, category, name, notes, prices, roles)
    return


def parse_url(url, data_canteen, today=False):
    canteen = LazyBuilder()

    data = urlopen(url).read().decode('utf-8')
    document = parse(data, 'lxml')

    dish = document.find(class_='neo-menu-single-dishes')
    if dish is not None:
        dishes = dish.find_all(name='tr', attrs={"data-canteen": data_canteen})
    else:
        dishes = []

    side = document.find(class_='neo-menu-single-modals')
    if side is not None:
        dishes = dishes + side.find_all(name='tr', attrs={"data-canteen": data_canteen})

    for dish in dishes:
        parse_dish(dish, canteen)

    return canteen.toXMLFeed()


parser = Parser('marburg', handler=parse_url,
                shared_args=['https://studentenwerk-marburg.de/essen-trinken/speisekarte/'])
parser.define('bistro', args=[460])
parser.define('mos-diner', args=[420])
parser.define('erlenring', args=[330])
parser.define('lahnberge', args=[340])
parser.define('cafeteria-lahnberge', args=[490])
