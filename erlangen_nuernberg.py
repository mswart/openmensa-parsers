#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import LazyBuilder

from utils import Parser

date_regex = re.compile('(?P<week_day>[A-Z][a-z])\ (?P<day>[0-9].)\.(?P<month>[0-9].)\.')
price_regex = re.compile('(?P<val>[0-9]*,[0-9].)')

roles = ('student', 'employee', 'other')

def parse_url(url, today=False):
    content = urlopen(url).read()
    document = parse(content)
    canteen = LazyBuilder()
    table = document.find_all('table')[0]

    def debug_print(food_type, food_description, priceing):
            if(priceing is None):
                print(date+': '+food_type+": "+food_description)
            else:
                print(date+': '+food_type+": "+food_description+" : ", end='')
                for e in priceing:
                    print(e, end=' ')
                print()

    def is_new_entry(tds):
        td = tds[0]
        return td.string is not None and date_regex.search(td.string) is not None

    def is_end_of_entry(tds):
        for td in tds:
            if(td.string is None or td.string.strip() != ''):
                return False
        return True

    def is_closed(tds):
        return is_new_entry(tds) and get_pricing(tds) is None

    def refactor_date(raw_date):
        now = datetime.datetime.now()
        day = date_regex.search(raw_date).group('day')
        month = date_regex.search(raw_date).group('month')
        year = now.year
        if month == '01' and now.month == 12:
            # if list depicts meals from this and the next year
            year+=1
        elif month == '12' and now.month == 1:
            # if list depicts meals form this and the last year
            year-=1
        return day+'.'+month+'.'+str(year)

    def parse_foot_type(td):
        type = ''
        if td.string is None:
            img = td.find_all('img')[0]
            src = img.get('src')
            if('msc' in src):
                type += 'MSC Fish '
            elif('vegan' in src):
                type += 'Vegan '
        else:
            if('R' in td.string):
                type += 'Rind '
            if('S' in td.string):
                type += 'Schwein '
            if('G' in td.string):
                type += 'Geflügel '
            if('V' in td.string):
                type += 'Vegetarisch '
            if('F' in td.string):
                type += 'Fisch '
            if('L' in td.string):
                type += 'Lamm '
            if('W' in td.string):
                type += 'Wild '
        return type

    def get_refs(td):
        return td.find_all('sup')


    def get_foot_description(td):
        refl = get_refs(td)
        description = td.text
        for ref in refl:
            description = description.replace(' '+ref.text, '', 1)
        if description[0] == ' ':
            description = description.replace(' ', '', 1)
        return description

    def get_pricing(tds):
        priceing = []
        for i in range(4, 7):
            raw_price = tds[i].string.strip()
            if raw_price == '':
                return None
            else:
                priceing.append(price_regex.search(raw_price).group('val'))
        return priceing


    # state helper
    inside_valide_entry = False
    date = ''

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if(is_new_entry(tds)):
            raw_date = tds[0].string
            date = refactor_date(raw_date)
            if(is_closed(tds)):
                canteen.setDayClosed(date)
            else:
                inside_valide_entry = True
        if(is_end_of_entry(tds)):
            inside_valide_entry = False
        elif inside_valide_entry:
            food_type = parse_foot_type(tds[2])
            food_description = get_foot_description(tds[3])
            prices = get_pricing(tds)
            #debug_print(food_type, food_description, priceing)
            canteen.addMeal(date, food_type, food_description, '', prices, roles if prices else None)
    return canteen.toXMLFeed()






parser = Parser('erlangen_nuernberg',
                handler=parse_url,
                shared_prefix='http://www.studentenwerk.uni-erlangen.de/verpflegung/de/')
parser.define('er-langemarck', suffix='sp-er-langemarck.shtml')
parser.define('er-sued', suffix='sp-er-sued.shtml')
parser.define('n-schuett', suffix='sp-n-schuett.shtml')
parser.define('n-regens', suffix='sp-n-regens.shtml')
parser.define('n-stpaul', suffix='sp-n-stpaul.shtml')
parser.define('n-mensateria', suffix='sp-n-mensateria.shtml')
parser.define('n-hohfederstr', suffix='sp-n-hohfederstr.shtml')
parser.define('n-baerenschanzstr', suffix='sp-n-baerenschanzstr.shtml')
parser.define('eichstaett', suffix='sp-eichstaett.shtml')
parser.define('ingolstadt', suffix='sp-ingolstadt.shtml')
parser.define('ansbach', suffix='sp-ansbach.shtml')
parser.define('triesdorf', suffix='sp-triesdorf.shtml')
