from bs4 import BeautifulSoup
import datetime
import re
import sys
from urllib.request import urlopen

from utils import Parser, EasySource, Source

# Taken from the filter menu on the website
note_descriptions = {
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

class Canteen(EasySource):
    def __init__(self, *args, id, open_id=None):
        super(Canteen, self).__init__(*args)
        self.id = id
        self.open_id = open_id
        self._data = None

    @Source.full_feed
    def parse_data(self, request):
        data = self.load_data()

        mensa = data.find("mensa", id=self.id)

        for day in mensa.find_all("day"):
            date = day["date"]
            for meal in day.find_all("meal"):
                if self.open_id is not None and meal["oeffnung"].strip() != self.open_id:
                    continue

                name = meal["meal"].strip()
                category = meal["kindname"].strip()
                if not name or not category:
                    continue

                notes = set()
                for key in ["kennzeichnung", "allergen_text", "zusatz_text"]:
                    if not meal[key]:
                        continue
                    for note in map(lambda e: e.strip(), meal[key].split(",")):
                        if not note:
                            continue
                        if note in note_descriptions:
                            notes.add(note_descriptions[note])
                        else:
                            print("Unknown note {}: {}, {}".format(note, date, name), file=sys.stderr)
                            notes.add(note)

                prices = {
                    'student': meal["price_stud"],
                    'employee': meal["price_empl"],
                    'other': meal["price_guest"],
                }
                self.feed.addMeal(date, category, name, notes=notes, prices=prices)

        return self.feed.toXMLFeed()

    def extract_metadata(self):
        data = self.load_data()
        mensa = data.find("mensa", id=self.id)

        address = re.match(
            r'^(?P<street>.*)\s+(?P<postcode>\d{5})\s+(?P<city>.+)$',
            mensa["address"]
        )

        canteen = self.feed
        canteen.name = mensa["showname"]
        if address is not None:
            canteen.address = "{}, {} {}".format(
                address.group("street").strip(),
                address.group("postcode"),
                address.group("city").strip(),
            )
            canteen.city = address.group("city").strip().capitalize()
        pass

    def load_data(self):
        # Cache the data for 15 min to not stress the API too much
        now = datetime.datetime.now()
        if self._data is None or now - self._data[1] > datetime.timedelta(minutes=15):
            content = urlopen(self.parser.shared_prefix).read()
            data = BeautifulSoup(content.decode('utf-8'), 'xml')
            self._data = (data, now)
        return self._data[0]

parser = Parser('ostniedersachsen', version="1.0", shared_prefix='http://api.stw-on.de/xml/mensa.xml')

braunschweig = parser.sub('braunschweig')
Canteen('mensa1-mittag', braunschweig, id="101", open_id="2")
Canteen('mensa1-abend', braunschweig, id="101", open_id="3")
Canteen('mensa360', braunschweig, id="111")
Canteen('mensa2', braunschweig, id="105")
Canteen('mensa2-cafeteria', braunschweig, id="106")
Canteen('hbk', braunschweig, id="120")
Canteen('bistro-nff', braunschweig, id="109")

Canteen('clausthal', parser, id="171")

hildesheim = parser.sub('hildesheim')
Canteen('uni', hildesheim, id="150")
Canteen('hohnsen', hildesheim, id="160")
Canteen('luebecker-strasse', hildesheim, id="153")

Canteen('holzminden', parser, id="163")

Canteen('lueneburg', parser, id="140")

Canteen('salzgitter', parser, id="200")

Canteen('suderburg', parser, id="134")

Canteen('wolfenbuettel', parser, id="130")

Canteen('wolfsburg', parser, id="112")
