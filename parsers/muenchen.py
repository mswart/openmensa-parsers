from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as parse
import re
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')

base = 'http://www.studentenwerk-muenchen.de/mensa'


def parse_url(url, today=False):
    canteen = LazyBuilder()

    # prices are stored on a separate page
    document = parse(urlopen(base + '/mensa-preise/').read(), 'lxml')
    prices = {}
    for tr in document.find('div', 'ce-bodytext').find_all('tr'):
        meal = tr.find('th')
        if not meal or not meal.text.strip():
            continue
        if len(tr.find_all('td', 'betrag')) < 3:
            continue
        if 'titel' in meal.attrs.get('class', []) or 'zeilentitel' in meal.attrs.get('class', []):
            continue
        meal = meal.text.strip()
        prices[meal] = {}
        for role, _id in [('student', 0), ('employee', 1), ('other', 2)]:
            price_html = tr.find_all('td', 'betrag')[_id].text
            price_search = price_regex.search(price_html)
            if price_search:
                prices[meal][role] = price_search.group('price')

    errorCount = 0
    date = datetime.date.today()
    while errorCount < 7:
        try:
            document = parse(urlopen(url.format(date)).read(), 'lxml')
            errorCount = 0
        except HTTPError as e:
            if e.code == 404:
                errorCount += 1
                date += datetime.timedelta(days=1)
                continue
            else:
                raise e

        # extract legend
        legend = {}
        legends = document.find('div', 'tx-stwm-speiseplan')
        additions = legends.find('div', 'c-schedule__filter-body')
        for table in additions.find_all('div', 'c-schedule__filter-item'):
            for ingredient in table.find('ul').find_all('li'):
                name = ingredient.find('dt').text.strip()
                description = ingredient.find('dd').text.strip()
                legend[name] = description
        for label in legends.find('ul', 'c-schedule__type-list').find_all('li'):
            name = label.find('dt').text.replace('(', '').replace(')', '').strip()
            description = label.find('dd').text.strip()
            legend[name] = description

        # extract meals
        mensa_data = document.find('ul', 'c-schedule__list')
        category = None
        for meal in mensa_data.find_all('li'):
            # update category or use previous one if not specified
            category_text = meal.find('dt', 'c-schedule__term').text.strip()
            if category_text:
                category = category_text

            data = meal.find('dd').find('p', 'js-schedule-dish-description')
            name = data.contents[0].strip() # name is the first text node
            if not name:
                continue

            # notes are contained in 3 boxes (type, additional, allergen) and
            # are comma-separated lists enclosed in brackets or parentheses
            notes = []
            for note in meal.find_all('span', 'c-schedule__marker'):
                note_text = note.find('span', 'u-text-sup').text \
                    .replace('(', '').replace(')', '') \
                    .replace('[', '').replace(']', '')
                notes += [n for n in note_text.split(',') if n]

            # some meals contain the GQB label in their name (instead of in notes)
            if '(GQB)' in name:
                name = name.replace('(GQB)', '').strip()
                notes.append('GQB')

            # add vegetarian/vegan notes
            if meal.find('span', attrs={'class': 'fleischlos'}):
                notes.append('vegetarisch')
            if meal.find('span', attrs={'class': 'vegan'}):
                notes.append('vegan')

            # the price for both meals is specified as Bio-/Aktionsgericht
            price_category = category \
                .replace('Aktionsessen', 'Bio-/Aktionsgericht') \
                .replace('Biogericht', 'Bio-/Aktionsgericht') \
                .strip()

            canteen.addMeal(date, category, name,
                [legend.get(n, n) for n in notes],
                prices.get(price_category, {})
            )

        date += datetime.timedelta(days=1)
        if today:
            break

    return canteen.toXMLFeed()


parser = Parser('muenchen', handler=parse_url, shared_prefix=base+'/speiseplan/')
parser.define('arcisstrasse', suffix='speiseplan_{}_421_-de.html')           #Mensa Arcisstraße
parser.define('garching', suffix='speiseplan_{}_422_-de.html')               #Mensa Garching
parser.define('leopoldstrasse', suffix='speiseplan_{}_411_-de.html')         #Mensa Leopoldstraße
parser.define('lothstrasse', suffix='speiseplan_{}_431_-de.html')            #Mensa Lothstraße
parser.define('martinsried', suffix='speiseplan_{}_412_-de.html')            #Mensa Martinsried
parser.define('pasing', suffix='speiseplan_{}_432_-de.html')                 #Mensa Pasing
parser.define('weihenstephan', suffix='speiseplan_{}_423_-de.html')          #Mensa Weihenstephan
parser.define('akademie', suffix='speiseplan_{}_455_-de.html')               #StuBistro Akademiestraße
parser.define('arcisstrasse-stubistro', suffix='speiseplan_{}_450_-de.html') #StuBistro Arcisstraße
parser.define('goethestrasse', suffix='speiseplan_{}_418_-de.html')          #StuBistro Goethestraße
parser.define('martinsried-stubistro', suffix='speiseplan_{}_415_-de.html')  #StuBistro Martinsried
parser.define('oberschleissheim', suffix='speiseplan_{}_419_-de.html')       #StuBistro Oberschleißheim
parser.define('oettingenstrasse', suffix='speiseplan_{}_424_-de.html')       #StuBistro Oettingenstraße
parser.define('rosenheim', suffix='speiseplan_{}_441_-de.html')              #StuBistro Rosenheim
parser.define('schellingstrasse', suffix='speiseplan_{}_416_-de.html')       #StuBistro Schellingstraße
parser.define('adalbertstrasse', suffix='speiseplan_{}_512_-de.html')        #StuCafé Adalbertstraße
parser.define('akademie-wst', suffix='speiseplan_{}_526_-de.html')           #StuCafé Akademie Weihenstephan
parser.define('boltzmannstrasse', suffix='speiseplan_{}_527_-de.html')       #StuCafé Boltzmannstraße
parser.define('cafeteria-garching', suffix='speiseplan_{}_524_-de.html')     #StuCafé in der Mensa Garching
parser.define('karlstrasse', suffix='speiseplan_{}_532_-de.html')            #StuCafé Karlstraße
