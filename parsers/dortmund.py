import re
import datetime
import urllib.request as rq

from urllib.parse import urlencode as urlencode
from bs4 import BeautifulSoup
from utils import Parser

from pyopenmensa.feed import LazyBuilder

# dictionary for categories
categories = {
    103: 'Tagesgericht',
    101: 'Menü 1',
    102: 'Menü 2',
    104: 'Vegetarisches Menü',
    105: 'Aktionsteller',
    106: 'Aktionsteller Fisch',
    107: 'Aktionsteller Vegan',
    108: 'Grillstation',
    109: 'Selfservice Station',
    115: 'Restaurant',
    116: 'Beilage',
    120: 'Menü 1',
    121: 'Menü 2',
    122: 'Menü 3',
    123: 'Menü 3',
    124: 'Vegetarisches Menü',
    125: 'Vegan',
    127: 'Aktionsteller',
    128: 'Schnelle Theke',
    130: 'Sonstige',
    131: 'Low Carb Teller',
    135: 'Pastatheke Pastaauswahl',
    136: 'Pastatheke Toppings',
    137: 'Pastatheke Saucen',
}

def getWeekdays(day):
    currentWeekday = day.weekday()
    week = []
    wstart = -currentWeekday
    wend = 7 - currentWeekday
    for d in range(wstart, wend):
        nday = day + datetime.timedelta(days=d)
        week.append(nday.isoformat())
    return week

def parse_url(url, today=False):
    canteen = LazyBuilder()

    canteen.extra_regex = re.compile('\((?P<extra>[0-9a-zA-Z]{1,3}'
                                     '(?:,[0-9a-zA-Z]{1,3})*)\)', re.UNICODE)

    legend_url = 'https://www.stwdo.de/mensa-co/allgemein/zusatzstoffe/'
    legend = parse_legend(legend_url)
    canteen.setLegendData(legend)

    day = datetime.date.today()
    week = getWeekdays(day)

    for wDay in week:
        py = {'tx_pamensa_mensa[date]' : wDay}
        payload = urlencode(py).encode('ascii')
        data = rq.urlopen(url, payload).read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        parse_day(canteen, soup, wDay)

    return canteen.toXMLFeed()

def parse_legend(url):
    data = rq.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')

    table = soup.find('table', { 'class' : 'table' })

    legend = {}

    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        key = td[0].text.strip()
        legend[key] = td[1].text.strip()

    return legend

def define_category(item, img):
    if 'fallback' in img['src']:
        return 'Unbekannt'

    if img is not None and len(img['title']) > 0:
        return img['title']
    else:
        catNumber = int(re.findall('[0-9]{3}', item['class'][2])[0])
        fallback = categories.get(130)
        return categories.get(catNumber, fallback)

def getAndFormatPrice(price):
    price = re.search('(\d+),(\d{2})', price)
    if price is not None:
        formatted = int(price.group(1) + price.group(2))
        return formatted
    else:
        return '-'

def parse_day(canteen, soup, wdate):
    mealsBody = soup.find('tbody', { 'class' : 'meals__tbody' })

    # Canteen seems to be closed...
    if mealsBody is None:
        return

    for meal in mealsBody.find_all('tr', { 'class' : 'meals__row' }):

        # This is needed for Food Fakultaet because there are subheadings
        if meal.find('th'):
            continue

        for item in meal.find_all('td'):
            for cssClass in item['class']:
                if 'category' in cssClass:
                    img = item.find('img')
                    category = define_category(item, img)
                elif 'title' in cssClass:
                    title = item.text.strip()
                elif 'supplies'in cssClass:
                    supplies = []
                    for supply in item.find_all('img'):
                        if supply['title']:
                            supplies.append(supply['title'])
                elif 'price'in cssClass:
                    priceTextContent = item.text
                    if 'S:' in priceTextContent:
                        student_price = getAndFormatPrice(priceTextContent)
                    elif 'B:' in priceTextContent:
                        staff_price = getAndFormatPrice(priceTextContent)
                    elif 'G:' in priceTextContent:
                        guest_price = getAndFormatPrice(priceTextContent)
        try:
            canteen.addMeal(wdate, category, title, notes=supplies, prices={'student': student_price, 'employee': staff_price, 'other': guest_price})
        except ValueError as e:
            if str(e) != "Meal names must not be empty": raise

parser = Parser('dortmund', handler=parse_url, shared_prefix='https://www.stwdo.de/mensa-cafes-und-catering/')

parser.define('tu-hauptmensa', suffix='tu-dortmund/hauptmensa/')
parser.define('tu-mensa-sued', suffix='tu-dortmund/mensa-sued/')
parser.define('tu-vital', suffix='tu-dortmund/vital/')
parser.define('tu-archeteria', suffix='tu-dortmund/archeteria/')
parser.define('tu-calla', suffix='tu-dortmund/restaurant-calla/')
parser.define('tu-food-fakultaet', suffix='tu-dortmund/food-fakultaet/')
parser.define('fh-mensa-max-ophuels-platz', suffix='fh-dortmund/max-ophuels-platz/')
parser.define('fh-mensa-sonnenstrasse', suffix='fh-dortmund/sonnenstrasse/')
parser.define('fh-kostbar', suffix='fh-dortmund/mensa-kostbar/')
parser.define('ism-mensa', suffix='ism/mensa-der-ism/')
parser.define('fernuni-mensa', suffix='hagen')
parser.define('fsw-snackit', suffix='fh-suedwestfalen/hagen/')
parser.define('fsw-canape', suffix='fh-suedwestfalen/iserlohn/')
parser.define('fsw-davinci', suffix='fh-suedwestfalen/meschede/')
parser.define('fsw-mensa', suffix='fh-suedwestfalen/soest/')
