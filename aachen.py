#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from bs4.element import NavigableString, Tag

from pyopenmensa.feed import OpenMensaCanteen, buildLegend

legend = None


def parse_day(canteen, day, data):
    # 1. menues
    note = data.find(id='note')
    if note:
        canteen.setDayClosed(day)
        return
    for menu in data.find(attrs={'class':'menues'}).find_all('tr'):
        # category:
        category = menu.find('td', attrs={'class':'category'}).text.strip()
        # split name and notes:
        name = ''
        notes = set()
        for namePart in menu.find('td', attrs={'class':'menue'}).children:
            if type(namePart) is NavigableString:
                name += namePart.string
            elif type(namePart) is Tag:
                notes.update(namePart.text.strip().split(','))
        name = name.strip()
        notes = [legend.get(n, n) for n in notes]
        # price:
        price = menu.find('td', attrs={'class':'price'}).text.strip()
        # store data
        canteen.addMeal(day, category, name, notes, price)


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
