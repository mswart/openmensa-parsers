from urllib.request import urlopen

from bs4 import BeautifulSoup as parse
from bs4.element import NavigableString, Tag
from ordered_set import OrderedSet

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen, buildLegend

legend = None


def add_meals_from_table(canteen, table, day):
    for item in table.find_all('tr'):
        category, name, notes, price_tag = parse_meal(item)
        canteen.addMeal(day, category, name, notes, price_tag)


def parse_meal(table_row):
    category = table_row.find('span', attrs={'class': 'menue-category'}).text.strip()

    description_elements = table_row.find('span', attrs={'class': 'menue-desc'})
    name, notes = parse_description(description_elements)

    price_tag = table_row.find('span', attrs={'class': 'menue-price'})
    if price_tag:
        price_tag = price_tag.text.strip()

    return category, name, notes, price_tag


def parse_description(description):
    name = ''
    notes = OrderedSet()
    for namePart in description.children:
        if type(namePart) is Tag and namePart.name == 'sup':
            notes.update(namePart.text.strip().split(','))
        else:
            name += namePart.string
    name = name.strip()
    notes = [legend.get(n, n) for n in notes if n]
    return name, notes


def parse_day(canteen, day, data):
    # 1. menues
    note = data.find(id='note')
    if note:
        canteen.setDayClosed(day)
        return
    add_meals_from_table(canteen, data.find(attrs={'class': 'menues'}), day)

    # 2. extras:
    extras_table = data.find(attrs={'class': 'extras'})

    if not extras_table:
        return
    add_meals_from_table(canteen, extras_table, day)


def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    # todo only for: Tellergericht, vegetarisch, Klassiker, Empfehlung des Tages:
    canteen.setAdditionalCharges('student', {'other': 1.5})

    document = parse(urlopen(url).read(), 'lxml')

    global legend
    regex = '\((?P<name>[\dA-Z]+)\)\s*(?P<value>[\w\s]+)'
    legend = buildLegend(legend, document.find(id='additives').text, regex=regex)

    days = ('montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag',
            'montagNaechste', 'dienstagNaechste', 'mittwochNaechste', 'donnerstagNaechste', 'freitagNaechste')
    for day in days:
        data = document.find('div', id=day)
        headline = document.find('a', attrs={'data-anchor': '#' + day})
        parse_day(canteen, headline.text, data)
    return canteen.toXMLFeed()


parser = Parser('aachen', handler=parse_url,
                shared_prefix='http://www.studentenwerk-aachen.de/speiseplaene/')
parser.define('academica', suffix='academica-w.html')
parser.define('ahorn', suffix='ahornstrasse-w.html')
parser.define('templergraben', suffix='templergraben-w.html')
parser.define('bayernallee', suffix='bayernallee-w.html')
parser.define('eups', suffix='eupenerstrasse-w.html')
parser.define('goethe', suffix='goethestrasse-w.html')
parser.define('vita', suffix='vita-w.html')
parser.define('zeltmensa', suffix='forum-w.html')
parser.define('juelich', suffix='juelich-w.html')
