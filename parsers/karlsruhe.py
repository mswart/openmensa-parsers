from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{4}-\d{2}-\d{2})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
notes_regex = re.compile('\[(?:(([A-Za-z0-9]+),?)+)\]$')

roles = ('student', 'other', 'employee', 'pupil')

extraLegend = {
    # Source: https://www.sw-ka.de/media/?file=4458_liste_aller_gesetzlich_ausweisungspflichtigen_zusatzstoffe_und_allergene_fuer_website_160218.pdf&download
    '1': 'mit Farbstoff',
    '2': 'mit Konservierungsstoff',
    '3': 'mit Antioxidationsmittel',
    '4': 'mit Geschmacksverstärker',
    '5': 'mit Phosphat',
    '6': 'Oberfläche gewachst',
    '7': 'geschwefelt',
    '8': 'Oliven geschwärzt',
    '9': 'mit Süßungsmitteln',
    '10': 'kann bei übermäßigem Verzehr abführend wirken',
    '11': 'enthält eine Phenylalaninquelle',
    '12': 'kann Restalkohol enthalten',
    '14': 'aus Fleischstücken zusammengefügt',
    '15': 'mit kakaohaltiger Fettglasur',
    '27': 'aus Fischstücken zusammengefügt',
    'Ca': 'Cashewnüsse',
    'Di': 'Dinkel',
    'Ei': 'Eier',
    'Er': 'Erdnüsse',
    'Fi': 'Fisch',
    'Ge': 'Gerste',
    'Gl': 'Glutenhaltiges Getreide',
    'Hf': 'Hafer',
    'Ha': 'Haselnüsse',
    'Ka': 'Kamut',
    'Kr': 'Krebstiere',
    'Lu': 'Lupine',
    'Ma': 'Mandeln',
    'ML': 'Milch/Laktose',
    'Nu': 'Schalenfrüchte/Nüsse',
    'Pa': 'Paranüsse',
    'Pe': 'Pekannüsse',
    'Pi': 'Pistazie',
    'Qu': 'Queenslandnüsse/Macadamianüsse',
    'Ro': 'Roggen',
    'Sa': 'Sesam',
    'Se': 'Sellerie',
    'Sf': 'Schwefeldioxid/Sulfit',
    'Sn': 'Senf',
    'So': 'Soja',
    'Wa': 'Walnüsse',
    'We': 'Weizen',
    'Wt': 'Weichtiere',
    'LAB': 'mit tierischem Lab',
    'GEL': 'mit Gelatine',
    'ICON=r_2.gif': 'enthält Rindfleisch',
    'ICON=2802_r_2.gif': 'enthält Rindfleisch',
    'ICON=ra_2.gif': 'enthält regionales Rindfleisch aus artgerechter Tierhaltung',
    'ICON=3302_rind_artgerecht.jpg': 'enthält regionales Rindfleisch aus artgerechter Tierhaltung',
    'ICON=2801_s_2.gif': 'enthält Schweinefleisch',
    'ICON=sa_2.gif': 'enthält regionales Schweinefleisch aus artgerechter Tierhaltung',
    'ICON=4456_schwein_artgerecht.jpg': 'enthält regionales Schweinefleisch aus artgerechter Tierhaltung',
    'ICON=vegetarian_2.gif': 'vegetarisches Gericht',
    'ICON=2803_vegetarian_2.gif': 'vegetarisches Gericht',
    'ICON=vegan_2.gif': 'veganes Gericht',
    'ICON=2804_vegan_2.gif': 'veganes Gericht',
    'ICON=bio_2.gif': 'kontrolliert biologischer Anbau mit EU Bio-Siegel / DE-Öko-007 Kontrollstelle',
    'ICON=3304_bio_neu_small.jpg': 'kontrolliert biologischer Anbau mit EU Bio-Siegel / DE-Öko-007 Kontrollstelle',
    'ICON=m_2.gif': 'MSC aus zertifizierter Fischerei',
    'ICON=2903_msc_logo_web.jpg': 'MSC aus zertifizierter Fischerei',
    'ICON=mv_2.gif': 'Mensa Vital',
    'ICON=4457_icon_mensavital.jpg': 'Mensa Vital'
}

def icon(src):
    return 'ICON=' + src.rsplit('/', 1).pop()

def parse_week(canteen, url, place_class=None):
    content = urlopen(url).read().decode('utf-8', errors='ignore')
    document = parse(content, features='lxml')
    legend = document.find('div', {'id': 'leg'})
    if legend:
        pass  # TODO Update legend

    if place_class:
        document = document.find(id=place_class)

    for day_a in document.find_all('a', rel=day_regex):
        day_data = document.find(id=day_a['href'].replace('#', ''))
        if not day_data:
            continue
        date = day_a['rel'][0]
        day_table = day_data.table
        if not day_table:
            continue
        if day_table.tbody:
            day_table = day_table.tbody
        canteen.clearDay(date)  # remove old data about this day
        for category_tr in day_table.children:
            if category_tr.name != 'tr':
                continue
            if len(category_tr) < 2:
                continue  # no meal
            category = category_tr.contents[0].text
            meal_table = category_tr.contents[1].table
            if meal_table.tbody:
                meal_table = meal_table.tbody
            for meal_tr in meal_table.children:
                if meal_tr.name != 'tr':
                    continue
                if len(list(meal_tr.children)) != 3:
                    #print('skipping category, unable to parse meal_table: {} tds'.format(len(list(meal_tr.children))))
                    continue
                if meal_tr.contents[1].find('span'):
                    name = meal_tr.contents[1].find('span').text  # Name without notes
                else:
                    name = meal_tr.contents[1].text
                # Add notes:
                sup = meal_tr.find('sup')
                if sup:
                    keys = sup.text.strip()[1:-1] if sup.text and sup.text.startswith('[') > 3 else ''
                    notes = [extraLegend[key] if key in extraLegend else key for key in keys.split(',') if key]
                else:
                    notes = []
                if meal_tr.contents[0].find('img'):
                    key = icon(meal_tr.contents[0].find('img')['src'])
                    if key in extraLegend:
                        notes.insert(0, extraLegend[key])

                canteen.addMeal(date, category, name, notes,
                                price_regex.findall(meal_tr.contents[2].text), roles)


def parse_url(url, place_class=None, today=False):
    canteen = OpenMensaCanteen()
    parse_week(canteen, url, place_class)
    day = datetime.date.today()
    old = -1
    day += datetime.date.resolution * 7
    if not today:
        parse_week(canteen, '{}?kw={}'.format(url, day.isocalendar()[1]), place_class)
    day += datetime.date.resolution * 7
    while not today and old != canteen.dayCount():
        old = canteen.dayCount()
        parse_week(canteen, '{}?kw={}'.format(url, day.isocalendar()[1]), place_class)
        day += datetime.date.resolution * 7
    return canteen.toXMLFeed()


parser = Parser('karlsruhe', handler=parse_url,
                shared_args=['http://www.studentenwerk-karlsruhe.de/de/essen/'])
parser.define('adenauerring', args=['canteen_place_1'])
parser.define('moltke', args=['canteen_place_2'])
parser.define('erzbergerstrasse', args=['canteen_place_3'])
parser.define('schloss-gottesaue', args=['canteen_place_4'])
parser.define('tiefenbronner-strasse', args=['canteen_place_5'])
parser.define('holzgartenstrasse', args=['canteen_place_6'])
