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
    116: 'Beilage',
    123: 'Menü 3',
    125: 'Vegan',
    128: 'Schnelle Theke',
    130: 'Sonstige',
    131: 'Low Carb Teller',
    135: 'Pastatheke',
}

def getAndFormatPrice(price):
    price = re.search('(\d+,\d{1,2})', price)
    formatted = re.sub('(\d+),(\d+)', r'\1.\2', price.group(0))
    return float(formatted)

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
    menu = soup.find('div', { 'class' : 'meals-wrapper' })
    mealsBody = menu.find('div', { 'class' : 'meals-body' })

    for meal in mealsBody.find_all('div', { 'class' : 'meal-item' }):
        for item in meal.find_all('div', { 'class' : 'item' }):
            cl1 = item['class'][1]
            if cl1 == 'category':
                catNumber = int(re.findall('[0-9]{3}', item['class'][2])[0])
                category = categories[catNumber]
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

print(parse_url('https://www.stwdo.de/mensa-co/tu-dortmund/hauptmensa/'))

parser = Parser('dortmund', handler=parse_url, shared_prefix='https://www.stwdo.de/mensa-co/')
parser.define('hauptmensa', suffix='tu-dortmund/hauptmensa/')
parser.define('mensa-sued', suffix='tu-dortmund/mensa-sued/')
parser.define('vital', suffix='tu-dortmund/vital/')
parser.define('archeteria', suffix='tu-dortmund/archeteria/')
parser.define('mensa-max-ophuels-platz', suffix='fh-dortmund/mensa-max-ophuels-platz/')
parser.define('mensa-sonnenstrasse', suffix='fh-dortmund/sonnenstrasse/')
parser.define('kostBar', suffix='fh-dortmund/mensa-kostbar/')
parser.define('food-fakultaet', suffix='tu-dortmund/food-fakultaet/')
parser.define('mensa-ism', suffix='ism/mensa-der-ism/')
