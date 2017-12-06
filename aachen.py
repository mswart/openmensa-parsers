from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from bs4.element import NavigableString, Tag

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen, buildLegend

legend = None

def add_extras_from_table(canteen, data, day):
    table = data.find('table', attrs={'class': 'extras'})
    if not table:
        return
    for item in table.find_all('tr'):
        # category
        category = item.find('span', attrs={'class': 'menue-category'}).text.strip()
        # split names and notes
        name = ''
        notes = set()

        descs = item.find('span', attrs={'class': 'menue-desc'})

        if not descs:
            return

        for namePart in descs.children:
            if (type(namePart) is Tag):
                pass #TODO: Add nutr-info to notes
            else:
                canteen.addMeal(day, category, namePart, notes)

def add_meals_from_table(canteen, data, day):
    table = data.find(attrs={'class': 'menues'})
    for item in table.find_all('tr'):
        # category
        category = item.find('span', attrs={'class': 'menue-category'}).text.strip()
        # split names and notes
        name = ''
        notes = set()

        descs = item.find('span', attrs={'class': 'expand-nutr'})

        if not descs:
            return

        for namePart in descs.children:
            if type(namePart) is NavigableString:
                name += namePart.string
            elif type(namePart) is Tag:
                if namePart.name == 'sup':
                    notes.update(namePart.text.strip().split(','))
                elif (namePart.string != None):
                    name += namePart.string
        name = name.replace('+', '', 1).strip()
        notes = [legend.get(n, n) for n in notes if n]

        price_tag = item.find('span', attrs={'class': 'menue-price'})
        if (name != ''):
            if not price_tag:
                canteen.addMeal(day, category, name, notes)
            else:
                canteen.addMeal(day, category, name, notes, price_tag.text.strip())

def parse_day(canteen, day, data):
    note = data.find(id='note')
    if note:
        canteen.setDayClosed(day)
        return

    add_meals_from_table(canteen, data, day)
    add_extras_from_table(canteen, data, day)

def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    # todo only for: Tellergericht, vegetarisch, Klassiker, Empfehlung des Tages:
    canteen.setAdditionalCharges('student', {'other': 1.5})

    document = parse(urlopen(url).read(), 'lxml')

    global legend
    regex = '\((?P<name>[\dA-Z]+)\)\s*(?P<value>[\w\s]+)'
    legend = buildLegend(legend, document.find(id='additives').text, regex=regex)

    day_boxes = document.findAll('div', {'class' : 'preventBreak'})
    for day_box in day_boxes:
        headline = day_box.find('a', attrs={'data-anchor': {'montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag'}})
        parse_day(canteen, headline.text, day_box)

    return canteen.toXMLFeed()


parser = Parser('aachen', handler=parse_url, #TODO: Update!
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
