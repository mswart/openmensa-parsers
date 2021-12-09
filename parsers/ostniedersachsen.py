from urllib.request import *

import json
import datetime
from pprint import pprint

from pyopenmensa.feed import LazyBuilder

from utils import Parser, Source

DATE_STRING = "%Y-%m-%d"
API_VERSION = "v1"
URL_BASE = 'https://sls.api.stw-on.de/%s/' % (API_VERSION)
LOCATIONS = {
    'sub': {
        'braunschweig': {
            'mensa1-mittag': {'id': 101, 'time': 'evening'},
            'mensa1-abend': {'id': 101, 'time': 'noon'},
            'mensa360': {'id': 111, 'time': 'all'},
            'mensa2': {'id': 105, 'time': 'all'},
            'mensa2-cafeteria': {'id': 106, 'time': 'all'},
            'hbk': {'id': 120, 'time': 'all'},
            'bistro-nff': {'id': 109, 'time': 'all'},
            'clausthal': {'id': 171, 'time': 'all'},
            'foodtruck-wilhelm': {'id': 194, 'time': 'all'},
            'foodtruck-katharine': {'id': 195, 'time': 'all'},
        },
        'hildesheim': {
            'uni': {'id': 150, 'time': 'all'},
            'hohnsen': {'id': 160, 'time': 'all'},
            'luebecker-strasse': {'id': 153, 'time': 'all'},
        }
    },
    'direct': {
        'clausthal': {'id': 171, 'time': 'all'},
        'holzminden': {'id': 163, 'time': 'all'},
        'lueneburg': {'id': 140, 'time': 'all'},
        'salzgitter': {'id': 200, 'time': 'all'},
        'salzgitter-bistro': {'id': 202, 'time': 'all'},
        'suderburg': {'id': 134, 'time': 'all'},
        'wolfenbuettel': {'id': 130, 'time': 'all'},
        'wolfsburg': {'id': 112, 'time': 'all'},
    }
}

# Taken from the filter menu on the website
NOTE_DESCRIPTIONS = {
    "VEGT": "Vegetarisch",
    "VEGA": "Vegan",
    "SCHW": "Schwein",
    "WILD": "Wild",
    "RIND": "Rind",
    "LAMM": "Lamm",
    "GEFL": "Geflügel",
    "FISH": "Fisch",
    "AT": "Artgerechte Tierhaltung",
    "BIO": "EU BIO Logo",
    "MV": "mensaVital",
    "NEU": "Neu!",
    # Allergens
    "1": "Farbstoff",
    "2": "Konservierungsstoff",
    "3": "Antioxidationsmittel",
    "4": "",
    "5": "geschwefelt",
    "6": "geschwärzt",
    "7": "gewachst",
    "8": "Phosphat",
    "9": "Süßungsmittel",
    "10": "Phenylalaninquelle",
    "11": "koffeinhaltig",
    "20": "Milcheiweiß",
    "21": "Milchpulver",
    "22": "Molkeneiweiß",
    "23": "Eiklar",
    "24": "Milch",
    "25": "Sahne",
    "53": "Erzeugnisse tierischen Ursprungs",
    "60": "Zucker und Süßungsmittel",
    "62": "konserviert mit Thiabendazol und Imazalil",
    "64": "kakaohaltige Fettglasur",
    # Additives
    "GL": "glutenhaltiges Getreide",
    "GL1": "Weizen",
    "GL2": "Roggen",
    "GL3": "Gerste",
    "GL4": "Hafer",
    "GL5": "Dinkel",
    "GL6": "Kamut",
    "KR": "Krebstiere",
    "EI": "Eier",
    "FI": "Fisch",
    "EN": "Erdnüsse",
    "SO": "Soja(bohnen)",
    "ML": "Milch (Laktose)",
    "SE": "Sesamsamen",
    "NU": "Schalenfrüchte",
    "NU1": "Mandeln",
    "NU2": "Haselnüsse",
    "NU3": "Walnüsse",
    "NU4": "Kaschunüsse",
    "NU5": "Pecanüsse",
    "NU6": "Paranüsse",
    "NU7": "Pistazien",
    "NU8": "Macadamianüsse",
    "SF": "Senf",
    "SL": "Sellerie",
    "SW": "Schwefeldioxid/Sulfite",
    "LU": "Lupine",
    "WT": "Weichtiere",
}


def parse_url(url, id, time, today=False):
    with urlopen(url) as response:
        data = json.loads(response.read().decode())

    canteens = {}
    for meal in data['meals']:
        if meal['location']['id'] not in canteens:
            canteens[meal['location']['id']] = {}
        if not meal['date'] in canteens[meal['location']['id']]:
            canteens[meal['location']['id']][meal['date']] = []
        canteens[meal['location']['id']][meal['date']].append(meal)

    canteen = LazyBuilder()
    for day, meals in canteens[id].items():
        date = datetime.datetime.strptime(day, DATE_STRING).date()

        if today and (datetime.date.today() != date):
            continue

        for meal in meals:
            if time != 'all' and meal['time'] != time:
                continue

            name = meal['name']
            category = meal['lane']['name']

            notes = set()
            if 'tags' in meal:
                for key in ["additives", "allergens", "categories", "special"]:
                    for note in meal['tags'][key]:
                        if not note:
                            continue
                        if note['id'] in NOTE_DESCRIPTIONS:
                            notes.add(NOTE_DESCRIPTIONS[note['id']])
                        else:
                            if 'name' not in note:
                                continue
                            notes.add(note['name'])

            prices = {}
            if 'price' in meal:
                for key, price in meal['price'].items():
                    if key == 'guest':
                        key = 'other'
                    prices[key] = price

            canteen.addMeal(date, category, name, notes, prices)

    return canteen.toXMLFeed()

parser = Parser('ostniedersachsen', handler=parse_url, shared_args=[URL_BASE + 'meals'])

for sub, locs in LOCATIONS['sub'].items():
    sub = parser.sub(sub)
    for name, loc in locs.items():
        sub.define(name, suffix=name, args=[loc['id'], loc['time']])

for name, loc in LOCATIONS['direct'].items():
    parser.define(name, suffix=name, args=[loc['id'], loc['time']])
