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
    return food_types.strip()

def get_refs(title):
    raw = ''.join(refs_regex.findall(title))
    return split_refs_regex.findall(raw)

def build_notes_string(title):
    food_is = ''
    food_contains = ''
    refs = get_refs(title)
    for r in refs:
        # parse food is footnotes
        if r == '1':
            food_is += 'mit Farbstoffen, '
        elif r == '2':
            food_is += 'mit Coffein '
        elif r == '4':
            food_is += 'mit Konservierungsstoff, '
        elif r == '5':
            food_is += 'mit Süßungsmittel, '
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
        elif r == '13':
            food_is += 'mit einer Phenylalaninquelle'
        elif r == '30':
            food_is += 'mit Fettglasur'
        elif r == 'Veg' or r == ' Veg':
            food_is += 'vegetarisch, '
        # parse allergic footnotes
        elif r == 'a1':
            food_contains += 'Gluten, '
        elif r == 'a2':
            food_contains += 'Krebstiere, '
        elif r == 'a3' or r == 'Ei':
            food_contains += 'Eier, '
        elif r == 'a4':
            food_contains += 'Fisch, '
        elif r == 'a5':
            food_contains += 'Erdnüsse, '
        elif r == 'a6' or r == 'So':
            food_contains += 'Soja, '
        elif r == 'a7' or r == 'Mi':
            food_contains += 'Milch/Laktose, '
        elif r == 'a8':
            food_contains += 'Schalenfrüchte, '
        elif r == 'a9' or r == 'Sel':
            food_contains += 'Sellerie, '
        elif r == 'a10' or r == 'Sen':
            food_contains += 'Senf, '
        elif r == 'a11' or r == 'Ses':
            food_contains += 'Sesam, '
        elif r == 'a12':
            food_contains += 'Schwefeldioxid/Sulfite, '
        elif r == 'a13':
            food_contains += 'Lupinen, '
        elif r == 'a14':
            food_contains += 'Weichtiere, '
        elif r == 'Wz':
            food_contains += 'Weizen, '
        elif r == 'Man':
            food_contains += 'Mandeln, '
        else:
            food_contains += 'undefinierte Chemikalie ' + r + ', '
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
        del nl[len(nl) - 1]
        nl[len(nl) - 1] = '.'
        return [''.join(nl)]
    else:
        return []

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
        date = time.strftime('%d.%m.%Y', time.localtime(int(day.get('timestamp'))))
        for item in day:
            title = item.find('title').text
            description = get_description(title)
            notes = build_notes_string(title)
            plist = [item.find('preis1').text, item.find('preis2').text, item.find('preis3').text]
            food_type = get_food_types(item.find('piktogramme').text)
            canteen.addMeal(date, food_type, description, notes, plist, roles)
    return canteen.toXMLFeed()



parser = Parser('erlangen_nuernberg',
                handler=parse_url,
                shared_prefix='https://www.max-manager.de/daten-extern/sw-erlangen-nuernberg/xml/')
parser.define('er-langemarck', suffix='mensa-lmp.xml')
parser.define('er-sued', suffix='mensa-sued.xml')
parser.define('n-schuett', suffix='mensa-inselschuett.xml')
parser.define('n-regens', suffix='mensa-regensburgerstr.xml')
parser.define('n-stpaul', suffix='mensateria-st-paul.xml')
parser.define('n-mensateria', suffix='mensateria-ohm.xml')
parser.define('n-hohfederstr', suffix='cafeteria-come-in.xml')
parser.define('n-baerenschanzstr', suffix='cafeteria-baerenschanzstr.xml')
parser.define('eichstaett', suffix='mensa-eichstaett.xml')
parser.define('ingolstadt', suffix='mensa-ingolstadt.xml')
parser.define('ansbach', suffix='mensa-ansbach.xml')
parser.define('triesdorf', suffix='mensateria-triesdorf.xml')
