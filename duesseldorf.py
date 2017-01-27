import re
from urllib.request import urlopen

from bs4 import BeautifulSoup as parse

from pyopenmensa.feed import OpenMensaCanteen
from utils import Parser

# this will match notes, e.g. "[R]" or "(1,10,12)"
legend_regex = re.compile('[\[(][ARFSVZ\d\,]+[\])]')

# this list was compiled from pdf available at http://www.stw-d.de/wp-content/uploads/2017/01/Zeichenerklaerung.pdf
legend_dict = {'R': 'mit Rindfleisch',
               'S': 'mit Schweinefleisch',
               'A': 'mit Alkohol',
               'F': 'fleischlos (enthält tierische Erzeugnisse)',
               'V': 'vegan',
               'Z': 'Bitte beachten Sie die Auszeichnung am Produkt',
               '1': 'Mit Konservierungsmittel',
               '2': 'mit Antioxidationsmittel',
               '3': 'mit Farbstoff',
               '4': 'mit Geschmacksverstärker',
               '5': 'mit Schwefel',
               '6': 'mit Phosphat',
               '7': 'geschwärzt',
               '8': 'gewachst',
               '9': 'mit Süßungsmittel',
               '10': 'enthält eine Phenylalaninquelle',
               '11': 'mit Säurungsmittel',
               '12': 'mit Stabilisatoren',
               '13': 'mit Phosphorsäure',
               '14': 'mit Nitritpökelsalz',
               '15': 'mit Milcheiweiß',
               '16': 'koffeinhaltig',
               '17': 'chininhaltig',
               '18': 'enthält Schwefeldioxid und Sulfite',
               '19': 'Milch und Milcherzeugnisse / enthält Laktose',
               '20': 'Glutenhaltiges Getreide sowie daraus hergestellte Erzeugnisse',
               '21': 'Soja und Sojaerzeugnisse',
               '22': 'Sellerie und Sellerieerzeugnisse',
               '23': 'Senf und Senferzeugnisse',
               '24': 'Sesamsamen und Sesamerzeugnisse',
               '25': 'Lupine und Lupinenerzeugnisse',
               '26': 'Erdnüsse und Erdnusserzeugnisse',
               '27': 'Fisch und Fischerzeugnisse',
               '28': 'Krebstiere und Krebstiererzeugnisse',
               '29': 'Weichtiere und Weichtiererzeugnisse',
               '30': 'Schalenfrüchte und Schalenfruchterzeugnisse',
               '31': 'Eier und Eierzeugnisse'
               }

# strings to be removed from meal title
remove_strings = ['- Preis je 100g:',
                  '- Preis ab:']


def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    document = parse(urlopen(url).read(), 'lxml')

    days = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag')
    for day in days:
        data = document.find('div', {'data-day': day})
        date = data.attrs['data-date']
        parse_day(canteen, date, data)

    return canteen.toXMLFeed()


def parse_day(canteen, date, data):
    # get meals from each category
    counters = data.find_all('div', class_='counter')
    add_meals_from_counter(canteen, counters, date)


def add_meals_from_counter(canteen, counters, date):
    for counter in counters:
        # get correct category name
        counter_name = counter.find('h2').text.strip()
        # find all menues for this category
        menu = counter.find('ul', 'menu')
        if menu and counter_name:
            # get contents of menu
            items = menu.find_all('li')
            # parse menu items
            meal, raw_legend = parse_menu_items(items)
            if not meal:
                continue
            # Studentenwerk Düsseldorf does not maintain a easily readable list of additives etc.
            # need to do our own parsing against a static list
            legend = parse_legend(raw_legend)
            # get prices for each role
            prices = parse_prices(counter.find('ul', 'price'))
            # add meal to list
            canteen.addMeal(date, counter_name, meal, notes=legend, prices=prices)


def parse_legend(raw_legend):
    verbose_legend = []  # we'll add parsed legend entries here
    for li in raw_legend:  # raw_legends contains a two dimensional array
        if li in legend_dict:
            # if found, add verbose description to list and cancel current iteration
            verbose_legend.append(legend_dict[li])
    return verbose_legend


def parse_menu_items(items):
    strings = []
    raw_legend = set()  # this will just contain lists of legend keys
    for item in items:
        # collect text from current item
        text = item.text.strip()
        if text not in ['', 'Mehr Informationen']:
            # find notes in text
            legend_tmp = legend_regex.findall(text)
            for li in legend_tmp:
                # remove notes from text to obtain a clean string
                text = text.replace(li, '').strip()
                # in addition, remove brackets left over after note deletion
                li = li[1:-1]
                # split notes in list and append master list
                li = li.split(',')
                raw_legend.update(li)
            strings.append(text)
    # join all strings and remove duplicate pricing information
    meal_name = ", ".join(strings)
    for sub in remove_strings:
        meal_name = meal_name.replace(sub, '')
    #  return result + raw legend
    return (meal_name.strip(), raw_legend)


def parse_prices(data):
    items = data.find_all('li')
    prices = {}
    # map roles
    roles = {'Studenten': 'student',
             'Bedienstete': 'employee',
             'Gäste': 'other'}
    for item in items:
        raw_role, price = item.text.split(':')
        if raw_role in roles:
            prices[roles[raw_role]] = price
    return prices


# name of canteens is suffix at the same time
canteens = ['mensa-universitaetsstrasse-duesseldorf',
            'mensa-kamp-lintfort',
            'mensa-campus-derendorf',
            'mensa-georg-glock-strasse-duesseldorf',
            'mensa-obergath-krefeld',
            'mensa-frankenring-krefeld',
            'mensa-sommerdeich-kleve',
            'mensa-rheydter-strasse-moenchengladbach',
            'restaurant-bar-campus-vita-duesseldorf',
            'essenausgabe-sued-duesseldorf',
            'kunstakademie-duesseldorf',
            'musikhochschule-duesseldorf']

parser = Parser('duesseldorf', handler=parse_url,
                shared_prefix='http://www.stw-d.de/gastronomie/speiseplaene/')

for canteen in canteens:
    parser.define(canteen, suffix=canteen)
