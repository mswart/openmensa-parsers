import requests
import re

from bs4 import BeautifulSoup
import datetime
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

def getAndFormatPrice(price):
    price = re.search('(\d+,\d{1,2})', price)
    if price != None:
        formatted = re.sub('(\d+),(\d+)', r'\1.\2', price.group(0))
        return float(formatted)
    else:
        return '-' 

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
    day = datetime.date.today()

    week = getWeekdays(day)

    for d in range(7):
        payload = {'tx_pamensa_mensa[date]' : week[d]}
        data = requests.get(url, payload)
        soup = BeautifulSoup(data.text, 'html.parser')

        parse_day(canteen, soup, week[d])

    legend_url = 'https://www.stwdo.de/mensa-co/allgemein/zusatzstoffe/'
    canteen.legend = parse_legend(legend_url)

    return canteen.toXMLFeed()

def parse_legend(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    table = soup.find('table', { 'class' : 'ce-table' })
    tbody = soup.find('tbody')

    legend = {}

    for tr in tbody.find_all('tr'):
        td = tr.find_all('td')
        legend[td[0].text] = td[1].text

    return legend

def parse_day(canteen, soup, wdate):
    global categories
    mealsBody = soup.find('div', { 'class' : 'meals-body' })

    for meal in mealsBody.find_all('div', { 'class' : 'meal-item' }):
        for item in meal.find_all('div', { 'class' : 'item' }):
            cl1 = item['class'][1]
            if cl1 == 'category':
                catNumber = int(re.findall('[0-9]{3}', item['class'][2])[0])
                if catNumber in categories:
                    category = categories[catNumber]
                else:
                    category = categories[130]
            elif cl1 == 'description':
                description = item.text.strip()
            elif cl1 == 'supplies':
                supplies = []
                for supply in item.find_all('img'):
                    supplies.append(supply['title'][0])
            elif cl1 == 'price':
                cl2 = item['class'][2]
                price = getAndFormatPrice(item.text)
                if cl2 == 'student':
                    student_price = price
                elif cl2 == 'staff':
                    staff_price = price
                elif cl2 == 'guest':
                    guest_price = price
        canteen.addMeal(wdate, category, description, notes=supplies, prices={'student': student_price, 'employee': staff_price, 'other': guest_price})

parser = Parser('dortmund', handler=parse_url, shared_prefix='https://www.stwdo.de/mensa-co/')

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
