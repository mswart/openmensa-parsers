from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
from bs4.element import Tag
import re

from utils import Parser

from pyopenmensa.feed import LazyBuilder, extractWeekDates

employeePrice = re.compile('Unibedienstetenzuschlag:? ?(?P<price>\d+[,.]\d{2}) ?€?')
otherPrice = re.compile('Gästezuschlag:? ?(?P<price>\d+[,.]\d{2}) ?€?')


def parse_week(url, canteen, mensa):
    document = parse(urlopen(url).read())
    # extra legends information
    canteen.setLegendData(text=document.find(text='Kennzeichnung: ').parent.next_sibling.get_text().replace('&nbsp;', ' '))
    # additional charges
    prices = {}
    for p in document.find_all('p'):
        match = employeePrice.search(p.text)
        if match:
            prices['employee'] = match.group('price')
        match = otherPrice.search(p.text)
        if match:
            prices['other'] = match.group('price')
    if len(prices) != 2:
        print('Could not extract addtional charges for employee and others')
    canteen.setAdditionalCharges('student', prices)
    # find
    mensa_data = document.find('h1', text=re.compile(mensa)).parent
    while type(mensa_data) != Tag or mensa_data.name != 'div'\
            or 'tx-cagcafeteria-pi1' not in mensa_data.get('class', []):
        mensa_data = mensa_data.next_sibling
    weekDays = extractWeekDates(mensa_data.find('h2').text)
    for day_headline in mensa_data.find_all('h3'):
        date = weekDays[day_headline.text]
        day_table = day_headline.next_sibling.next_sibling
        for tr_menu in day_table.tbody.find_all('tr'):
            category = tr_menu.find_all('td')[0].text.strip()
            name = tr_menu.find_all('td')[1].text.replace('\r\n', ' ').strip()
            canteen.addMeal(date, category, name, [], tr_menu.find_all('td')[2].text)


def parse_url(url, mensa, *weeks, today):
    canteen = LazyBuilder()
    for week in weeks:
        parse_week(url + week, canteen, mensa)
        if today:
            break
    return canteen.toXMLFeed()


parser = Parser('marburg', handler=parse_url,
                shared_args=['http://www.studentenwerk-marburg.de/essen-trinken/speiseplan/'])
parser.define('bistro', args=['Speiseplan.*Bistro', 'diese-woche-bistro.html', 'naechste-woche-bistro.html'])
parser.define('mos-diner', args=['Speiseplan.*Diner', 'diese-woche-mos-diner.html'])
parser.define('erlenring', args=['Mensa Erlenring', 'diese-woche-mensa-erlenring-und-lahnberge.html',
              'naechste-woche-mensa-erlenring-und-lahnberge.html'])
parser.define('lahnberge', args=['Mensa Lahnberge', 'diese-woche-mensa-erlenring-und-lahnberge.html',
              'naechste-woche-mensa-erlenring-und-lahnberge.html'])
