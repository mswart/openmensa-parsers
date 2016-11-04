from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from bs4.element import NavigableString, Tag

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen, buildLegend

legend = None


def parse_day(canteen, day, data):
    # 1. menues
    note = data.find(id='note')
    if note:
        canteen.setDayClosed(day)
        return
    for menu in data.find(attrs={'class': 'menues'}).find_all('tr'):
        # category:
        category = menu.find('span', attrs={'class': 'menue-category'}).text.strip()
        # split name and notes:
        name = ''
        notes = set()
        for namePart in menu.find('span', attrs={'class': 'menue-desc'}).children:
            if type(namePart) is NavigableString:
                name += namePart.string
            elif type(namePart) is Tag:
                notes.update(namePart.text.strip().split(','))
        name = name.strip()
        notes = [legend.get(n, n) for n in notes]
        # price:
        price = menu.find('span', attrs={'class': 'menue-price'}).text.strip()
        # store data
        canteen.addMeal(day, category, name, notes, price)

    # 2. extras:
    if not data.find(attrs={'class': 'extras'}):
        return
    for extra in data.find(attrs={'class': 'extras'}).find_all('tr'):
        category = extra.find('span', attrs={'class': 'menue-category'}).text.strip()
        name = ''
        notes = set()
        for namePart in extra.find('span', attrs={'class': 'menue-desc'}).children:
            if type(namePart) is NavigableString:
                name += namePart.string
            elif type(namePart) is Tag:
                if 'or' in namePart.get('class', []):
                    name += namePart.string
                else:
                    notes.update(namePart.text.strip().split(','))
        name = name.strip()
        notes = [legend.get(n, n) for n in notes]
        canteen.addMeal(day, category, name, notes)


def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    # todo only for: Tellergericht, vegetarisch, Klassiker, Empfehlung des Tages:
    canteen.setAdditionalCharges('student', {'other': 1.5})

    document = parse(urlopen(url).read())

    global legend
    regex = '(?P<name>(\d|[A-Z])+)\)\s*' + \
            '(?P<value>\w+((\s+\w+)*[^0-9)]))'
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
