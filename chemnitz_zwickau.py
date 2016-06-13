#!python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime

from utils import Parser

from pyopenmensa.feed import LazyBuilder

# http://www.swcz.de/fileadmin/mediamanager/Formulare_Dokumente/Verpflegung/Zusatzstoffe_und_Allergene.pdf

legend = {
    '1': 'mit Farbstoff',
    '2': 'mit Konservierungsstoff',
    '3': 'mit Antioxidationsmittel',
    '4': 'mit Geschmacksverstärker',
    '5': 'geschwefelt',
    '6': 'geschwärzt',
    '7': 'gewachst',
    '8': 'mit Phosphat',
    '9': 'mit Süßungsmittel',
    '10': 'phenylalaninhaltig',
    '11': 'koffeinhaltig',
    '12': 'chininhaltig',
    '13': 'Glutenhaltiges Getreide',
    '14': 'Krebstiere',
    '15': 'Eier',
    '16': 'Fisch',
    '17': 'Erdnüsse',
    '18': 'Soja',
    '19': 'Milch',
    '20': 'Schalenfrüchte/Nüsse',
    '21': 'Sellerie',
    '22': 'Senf',
    '23': 'Sesam',
    '24': 'Sulfit/Schwefel',
    '25': 'Lupine',
    '26': 'Weichtiere',
    '35': 'enthält Azofarbstoffe',
    '36': 'mit Molkeneiweiß',
    '37': 'mit Milchpulver',
    '38': 'mit Milcheiweiß',
    '39': 'mit Eiklar',
    '40': 'unter Verwendung von Milch',
    '41': 'unter Verwendung von Sahne',
    '43': 'mit kakaohaltiger Fettglasur',
    '44': 'mit Alkohol',
    '45': 'mit Gelatine',
    '46': 'mit Karmin E120',
    '47': 'mit tierischem Lab',
    '48': 'mit Honig',
    '49': 'mit Knoblauch',
    '51': 'Schwein',
    '52': 'Rind',
    '53': 'Lamm',
    '54': 'Geflügel',
    '55': 'Wild',
    '56': 'Fisch'
    }


def parse_day(canteen, url, date):
    content = urlopen(url).read()

    soup = BeautifulSoup(content, 'xml')

    rolesDict = {"S": "student", "M": "employee", "G": "other"}

    for essen in soup.find_all('essen'):
        category = essen['kategorie'] if essen.has_attr('kategorie') else ""
        if not essen.deutsch:
            continue
        name = essen.deutsch.string

        notes = []
        if essen.has_attr('vegetarisch') and essen['vegetarisch'] == 'true':
            notes = ['vegetarisch']

        price = essen.find('pr', gruppe="Preis")
        if price and price.string:
            prices = [price.string, price.string, price.string]
            roles = rolesDict.values()
        else:
            prices = []
            roles = []
            for group, role in rolesDict.items():
                price = essen.find('pr', gruppe=group)
                if (price and price.string):
                    prices.append(price.string)
                    roles.append(role)
        canteen.addMeal(date, category, name, notes, prices, roles)


def parse_url(url, today=False):
    global legend
    canteen = LazyBuilder()
    canteen.setLegendData(legend)
    day = datetime.date.today()
    emptyCount = 0
    totalCount = 0
    while emptyCount < 7 and totalCount < 32:
        if not parse_day(canteen, '{}&tag={}&monat={}&jahr={}'
                         .format(url, day.day, day.month, day.year),
                         day.strftime('%Y-%m-%d')):
            emptyCount += 1
        else:
            emptyCount = 0
        if today:
            break
        totalCount += 1
        day += datetime.date.resolution
    return canteen.toXMLFeed()


parser = Parser('chemnitz_zwickau', handler=parse_url,
                shared_prefix='http://www.swcz.de/bilderspeiseplan/xml.php?plan=')
parser.define('mensa-reichenhainer-strasse', suffix='1479835489')
parser.define('mensa-strasse-der-nationen', suffix='773823070')
parser.define('mensa-ring', suffix='4')
parser.define('mensa-scheffelberg', suffix='3')
parser.define('cafeteria-reichenhainer-strasse', suffix='7')
parser.define('cafeteria-strasse-der-nationen', suffix='6')
parser.define('cafeteria-ring', suffix='5')
parser.define('cafeteria-scheffelberg', suffix='8')
