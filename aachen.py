from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from bs4.element import NavigableString, Tag

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen, buildLegend

legend = None


def add_meals_from_table(canteen, table, day):
    for item in table.find_all('tr'):
        # category
        category = item.find('span', attrs={'class': 'menue-category'}).text.strip()
        # split names and notes
        name = ''
        notes = set()
        for namePart in item.find('span', attrs={'class': 'menue-desc'}).children:
            if type(namePart) is NavigableString:
                name += namePart.string
            elif type(namePart) is Tag:
                if namePart.name == 'sup':
                    notes.update(namePart.text.strip().split(','))
                else:
                    name += namePart.string
        name = name.strip()
        notes = [legend.get(n, n) for n in notes]
        price_tag = item.find('span', attrs={'class': 'menue-price'})
        if not price_tag:
            canteen.addMeal(day, category, name, notes)
        else:
            canteen.addMeal(day, category, name, notes, price_tag.text.strip())


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
