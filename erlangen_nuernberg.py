#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime
import traceback
import sys

from pyopenmensa.feed import LazyBuilder

from utils import Parser

date_regex = re.compile('(?P<week_day>[A-Z][a-z])\ (?P<day>[0-9].)\.(?P<month>[0-9].)')
price_regex = re.compile('(?P<val>[0-9]*,[0-9].)')

roles = ('student', 'employee', 'other')

def parse_url(url, today=False):
    content = urlopen(url).read()
    document = parse(content, "lxml")
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

    def is_action_entry(td):
        return td.text == 'Aktion'

    def is_closed(tds):
        return is_new_entry(tds) and get_pricing(tds, 4, 7) is None

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
            if len(td.find_all('img')) == 0:
                return None
            else:
                img = td.find_all('img')[0]
                src = img.get('src')
                if('msc' in src):
                    type += 'Fish MSC '
                elif('vegan' in src):
                    type += 'Vegan '
        #Sometimes none categorized food is possible, therfore we need to cover this,
        #otherwhise openmensa.org will faile dueto an empty tag.
        elif(td.string.strip() == ''):
            type += 'Tipp '
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
        tl = list(type)
        del tl[len(tl)-1]
        return ''.join(tl)

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

    def get_notes(td):
        refl = get_refs(td)
        strl = []
        for ref in refl:
            strl.extend(ref.string.split(','))
        strl = list(set(strl))
        return strl

    def build_notes_string(td):
        refs = get_notes(td)
        food_is = ''
        food_contains = ''
        for r in refs:
            # parse food is footnotes
            if r == '1':
                food_is += 'mit Farbstoffen, '
            elif r == '4':
                food_is += 'geschwärzt, '
            elif r == '7':
                food_is += 'mit Antioxidationsmittel, '
            elif r == '8':
                food_is += 'mit Geschmacksverstärker, '
            elif r == '9':
                food_is += 'geschwefelt, '
            elif r == '10':
                food_is += 'geschwärzt, '
            elif r == '11':
                food_is += 'gewachst, '
            elif r == '12':
                food_is += 'mit Phosphat, '
            elif r == '5':
                food_is += 'mit Süßungsmittel, '
            # parse allergic footnotes
            elif r == 'a1':
                food_contains += 'Gluten, '
            elif r == 'a2':
                food_contains += 'Krebstiere, '
            elif r == 'a3':
                food_contains += 'Eier, '
            elif r == 'a4':
                food_contains += 'Fisch, '
            elif r == 'a5':
                food_contains += 'Erdnüsse, '
            elif r == 'a6':
                food_contains += 'Soja, '
            elif r == 'a7':
                food_contains += 'Milch/Laktose, '
            elif r == 'a8':
                food_contains += 'Schalenfrüchte, '
            elif r == 'a9':
                food_contains += 'Sellerie, '
            elif r == 'a10':
                food_contains += 'Senf, '
            elif r == 'a11':
                food_contains += 'Sesam, '
            elif r == 'a12':
                food_contains += 'Schwefeldioxid/Sulfite, '
            elif r == 'a13':
                food_contains += 'Lupinen, '
            elif r == 'a14':
                food_contains += 'Weichtiere, '
            else:
                food_contains += 'undefinierte Chemikalien:'+r+', '
        notes = ''
        if food_is != '':
            notes += 'Gericht ist ' + food_is
        if food_contains != '':
            if food_is == '':
                notes += 'Gericht enthält '
            else:
                notes += 'und enthält '
            notes += food_contains
        if notes != '':
            nl = list(notes)
            del nl[len(nl)-1]
            nl[len(nl)-1] = '.'
            notes = ''.join(nl)
        return notes

    def get_pricing(tds, f, t):
        priceing = []
        #sometimes we dont don't get 7 elements, than this might be a special day
        if len(tds) < 7:
            return None
        for i in range(f, t):
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
            try:
                raw_date = tds[0].string
                date = refactor_date(raw_date)
                if(is_closed(tds)):
                    # sometismes a canteen might look closed but actually its spargeltage
                    if "Spargeltage" in tds[3].text:
                        canteen.addMeal(date, "Spargel", "Spargel Tag", ["Spargel und andere Gerichte."], None, None)
                    else:
                        canteen.setDayClosed(date)
                else:
                    inside_valide_entry = True
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
        if(is_end_of_entry(tds)):
            inside_valide_entry = False
        elif inside_valide_entry:
            try:
                notes = []
                if is_action_entry(tds[0]):
                    food_type = parse_foot_type(tds[1])
                    food_description = get_foot_description(tds[2])
                    notes_string = build_notes_string(tds[2])
                    if(notes_string != ""):
                        notes.append(notes_string)
                    prices = get_pricing(tds, 3, 6)


                    canteen.addMeal(date, 'Aktion: '+food_type, food_description, notes, prices, roles if prices else None)
                else:
                        food_type = parse_foot_type(tds[2])
                        food_description = get_foot_description(tds[3])
                        notes_string = build_notes_string(tds[3])
                        if(notes_string != ""):
                            notes.append(notes_string)
                        prices = get_pricing(tds, 4, 7)
                        if food_type is not None:
                            canteen.addMeal(date, food_type, food_description, notes, prices, roles if prices else None)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())

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
