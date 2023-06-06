from urllib.request import *

import time
import re
import xml.etree.ElementTree as ET

from pyopenmensa.feed import LazyBuilder

from utils import Parser

refs_regex = re.compile('(\([ ,a-zA-Z0-9]*\))')
split_refs_regex = re.compile('[\(,]([ a-zA-Z0-9]*)')
remove_refs_regex = re.compile('\([ ,a-zA-Z0-9]*\)')


roles = ('student', 'employee', 'other')


def get_food_types(piktogramme):
    fs = piktogramme
    food_types = ''
    if fs is None:
        return 'Sonstiges'
    if 'R.png' in fs:
        food_types += 'Rind '
    if 'S.png' in fs:
        food_types += 'Schwein '
    if 'G.png' in fs:
        food_types += 'Geflügel '
    if 'V.png' in fs:
        food_types += 'Vegetarisch '
    if 'F.png' in fs:
        food_types += 'Fisch '
    if 'L.png' in fs:
        food_types += 'Lamm '
    if 'W.png' in fs:
        food_types += 'Wild '
    if 'veg.png' in fs:
        food_types += 'Vegan '
    if 'MSC.png' in fs:
        food_types += 'MSC Fisch '
    if 'CO2.png' in fs:
        food_types += 'CO2 neutral '
    if 'Gf.png' in fs:
        food_types += 'Glutenfrei '
    if 'MV.png' in fs:
        food_types += 'mensaVital '
    if 'B.png' in fs:
        food_types += 'Biologischer Anbau '
    return food_types.strip()


def get_refs(title):
    raw = ''.join(refs_regex.findall(title))
    return split_refs_regex.findall(raw)


def build_notes_string(title):
    food_is = []
    food_contains = []
    refs = get_refs(title)
    for r in refs:
        # parse food is footnotes
        if r == '1':
            food_is.append('mit Farbstoffen')
        elif r == '2':
            food_is.append('mit Coffein')
        elif r == '4':
            food_is.append('mit Konservierungsstoff')
        elif r == '5':
            food_is.append('mit Süßungsmittel')
        elif r == '7':
            food_is.append('mit Antioxidationsmittel')
        elif r == '8':
            food_is.append('mit Geschmacksverstärker')
        elif r == '9':
            food_is.append('geschwefelt')
        elif r == '10':
            food_is.append('geschwärzt')
        elif r == '11':
            food_is.append('gewachst')
        elif r == '12':
            food_is.append('mit Phosphat')
        elif r == '13':
            food_is.append('mit einer Phenylalaninquelle')
        elif r == '30':
            food_is.append('mit Fettglasur')
        elif r == 'Veg' or r == ' Veg':
            food_is.append('ist vegetarisch')
        # parse allergic footnotes
        elif r == 'a1':
            food_contains.append('mit Gluten')
        elif r == 'a2' or r == 'Kr':
            food_contains.append('mit Krebstieren')
        elif r == 'a3' or r == 'Ei':
            food_contains.append('mit Eier')
        elif r == 'a4':
            food_contains.append('mit Fisch')
        elif r == 'a5' or r == 'Er':
            food_contains.append('mit Erdnüsse')
        elif r == 'a6' or r == 'So':
            food_contains.append('mit Soja')
        elif r == 'a7' or r == 'Mi':
            food_contains.append('mit Milch/Laktose')
        elif r == 'a8':
            food_contains.append('mit Schalenfrüchte')
        elif r == 'a9' or r == 'Sel':
            food_contains.append('mit Sellerie')
        elif r == 'a10' or r == 'Sen':
            food_contains.append('mit Senf')
        elif r == 'a11' or r == 'Ses':
            food_contains.append('mit Sesam')
        elif r == 'a12' or r == 'Su':
            food_contains.append('mit Schwefeldioxid/Sulfite')
        elif r == 'a13':
            food_contains.append('mit Lupinen')
        elif r == 'a14' or r == 'We':
            food_contains.append('mit Weichtiere')
        elif r == 'Wz':
            food_contains.append('mit Weizen')
        elif r == 'Man':
            food_contains.append('mit Mandeln')
        elif r== 'Ro':
            food_contains.append('mit Roggen')
        elif r== 'Ge':
            food_contains.append('mit Gerste')
        elif r== 'Hf':
            food_contains.append('mit Hafer')
        elif r== 'Hs':
            food_contains.append('mit Haselnüssen')
        elif r == 'Wa':
            food_contains.append('mit Walnüssen')
        elif r== 'Ka':
            food_contains.append('mit Cashew-Nüssen')
        elif r== 'Pe':
            food_contains.append('mit Pekannüssen')
        elif r== 'Pa':
            food_contains.append('mit Paranüssen')
        elif r== 'Pi':
            food_contains.append('mit Pistazien')
        elif r== 'Mac':
            food_contains.append('mit Macadamia-Nüssen')
        else:
            food_contains.append('mit undefiniertem Allergen ' + r)
    return food_contains


def get_description(title):
    raw = remove_refs_regex.split(title)
    return ''.join(raw)


def parse_url(url, today=False):
    canteen = LazyBuilder()
    try:
        xml_data = urlopen(url).read()
    except Exception:
        return canteen.toXMLFeed()
    root = ET.fromstring(xml_data)
    for day in root:
        date = time.strftime('%d.%m.%Y',
                             time.localtime(int(day.get('timestamp'))))
        for item in day:
            title = item.find('title').text
            description = get_description(title)
            notes = build_notes_string(title)
            plist = [item.find('preis1').text,
                     item.find('preis2').text,
                     item.find('preis3').text]
            food_type = get_food_types(item.find('piktogramme').text)
            print(f"[{food_type}]")
            canteen.addMeal(date, food_type, description, notes, plist, roles)
    return canteen.toXMLFeed()


parser = Parser('erlangen_nuernberg',
                handler=parse_url,
                shared_prefix= 'https://www.max-manager.de/daten-extern/sw-erlangen-nuernberg/xml/')
parser.define('er-langemarck', suffix='mensa-lmp.xml')
parser.define('er-sued', suffix='mensa-sued.xml')
parser.define('er-koch', suffix='cafeteria-kochstr.xml')
parser.define('er-suedblick', suffix='cafeteria-suedblick.xml') # currently no data
parser.define('er-erwinrommel', suffix='wohnanlage-erwin-rommel-str.xml')
parser.define('er-hartmann', suffix='wohnanlage-hartmannstr.xml') # currently no data
parser.define('n-schuett', suffix='mensa-inselschuett.xml')
parser.define('n-regens', suffix='mensa-regensburgerstr.xml')
parser.define('n-stpeter', suffix='wohnanlage-st-peter.xml')
parser.define('n-stpaul', suffix='mensateria-st-paul.xml') # currently no data
parser.define('n-mensateria', suffix='mensateria-ohm.xml')
parser.define('n-veilhof', suffix='cafeteria-veilhofstr.xml')
parser.define('n-hohfeder', suffix='cafeteria-come-in.xml')
parser.define('n-langegasse', suffix='cafeteria-wiso.xml') # currently no data
parser.define('n-baerensch', suffix='cafeteria-baerenschanzstr.xml')
parser.define('n-bing', suffix='cafeteria-bingstr.xml')
parser.define('eichstaett', suffix='mensa-eichstaett.xml')
parser.define('ingolstadt', suffix='mensa-ingolstadt.xml')
parser.define('ansbach', suffix='mensa-ansbach.xml')
parser.define('triesdorf', suffix='mensateria-triesdorf.xml')
