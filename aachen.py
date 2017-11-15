from urllib.request import urlopen

from bs4 import BeautifulSoup as parse
from bs4.element import Tag

from pyopenmensa.feed import OpenMensaCanteen, buildLegend
from utils import Parser


def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    document = parse(urlopen(url).read(), 'lxml')

    # todo only for: Tellergericht, vegetarisch, Klassiker, Empfehlung des Tages:
    canteen.setAdditionalCharges('student', {'other': 1.5})
    canteen.legend = parse_legend(document)

    parse_all_days(canteen, document)

    return canteen.toXMLFeed()


def parse_legend(document):
    regex = '\((?P<name>[\dA-Z]+)\)\s*(?P<value>[\w\s]+)'
    # bypass automatic notes extraction in `OpenMensaCanteen.addMeal()`:
    return buildLegend(text=document.find(id='additives').text, regex=regex)


def parse_all_days(canteen, document):
    days = ('montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag',
            'montagNaechste', 'dienstagNaechste', 'mittwochNaechste', 'donnerstagNaechste', 'freitagNaechste')
    for day in days:
        data = document.find('div', id=day)
        day_header = document.find('a', attrs={'data-anchor': '#' + day})
        parse_day(canteen, day_header.text, data)


def parse_day(canteen, day, data):
    if is_closed(data):
        canteen.setDayClosed(day)
        return

    meals_table = data.find(attrs={'class': 'menues'})
    add_meals_from_table(canteen, meals_table, day)

    extras_table = data.find(attrs={'class': 'extras'})
    add_meals_from_table(canteen, extras_table, day)


def is_closed(data):
    note = data.find(id='note')
    if note:
        return True
    else:
        return False


def add_meals_from_table(canteen, table, day):
    for item in table.find_all('tr'):
        category, name, notes, price_tag = parse_meal(item, canteen.legend)
        canteen.addMeal(day, category, name, notes, prices=price_tag)


def parse_meal(table_row, legend):
    category = table_row.find('span', attrs={'class': 'menue-category'}).text.strip()

    description_container = table_row.find('span', attrs={'class': 'menue-desc'})
    name, notes = parse_description(description_container, legend)

    price_tag = table_row.find('span', attrs={'class': 'menue-price'})
    if price_tag:
        price_tag = price_tag.text.strip()

    return category, name, notes, price_tag


def parse_description(description, legend):
    name = ''
    notes = set()
    for namePart in description.children:
        if type(namePart) is Tag and namePart.name == 'sup':
            notes.update(namePart.text.strip().split(','))
        else:
            name += namePart.string
    name = name.strip()
    notes = [legend.get(n, n) for n in notes if n]
    return name, notes


parser = Parser(
    'aachen',
    handler=parse_url,
    shared_prefix='http://www.studentenwerk-aachen.de/speiseplaene/',
)

parser.define('academica', suffix='academica-w.html')
parser.define('ahorn', suffix='ahornstrasse-w.html')
parser.define('templergraben', suffix='templergraben-w.html')
parser.define('bayernallee', suffix='bayernallee-w.html')
parser.define('eups', suffix='eupenerstrasse-w.html')
parser.define('goethe', suffix='goethestrasse-w.html')
parser.define('vita', suffix='vita-w.html')
parser.define('zeltmensa', suffix='forum-w.html')
parser.define('juelich', suffix='juelich-w.html')
