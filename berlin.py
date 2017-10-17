#!/usr/bin/env python3

from pyopenmensa.feed import BaseBuilder, buildPrices
from bs4 import BeautifulSoup
from utils import Parser
import datetime
import urllib

roles = ('student', 'employee', 'other')
img_map = {
    'ampel_gruen_70x65.png': 'Grün (Ampel)',
    'ampel_gelb_70x65.png': 'Gelb (Ampel)',
    'ampel_rot_70x65.png': 'Rot (Ampel)',
    '15.png': 'vegan',
    '43.png': 'Klimaessen',
    '1.png': 'vegetarisch',
    '18.png': 'bio',
    '38.png': 'MSC',
}
# mapping taken from https://github.com/ekeih/OmNomNom/blob/144ee35c51e2d82ff18eef79a46137d44cb28609/canteens/studierendenwerk.py
mapping = {
    534: {"name": "Mensa ASH Berlin Hellersdorf", "command": "ash_hellersdorf"},
    535: {"name": "Mensa Beuth Hochschule für Technik Kurfürstenstraße", "command": "beuth_kurfuerstenstr"},
    527: {"name": "Mensa Beuth Hochschule für Technik Luxemburger Straße", "command": "beuth_luxembugerstr"},
    537: {"name": "Mensa Charité Zahnklinik", "command": "charite_zahnklinik"},
    529: {"name": "Mensa EHB Teltower Damm", "command": "ehb_teltower_damm"},
    271: {"name": "Mensa FU Herrenhaus Düppel", "command": "fu_dueppel"},
    322: {"name": "Mensa FU II Otto-von-Simson-Straße", "command": "fu_2"},
    528: {"name": "Mensa FU Lankwitz Malteserstraße", "command": "fu_lankwitz"},
    531: {"name": "Mensa HfM Charlottenstraße", "command": "hfm_charlottenstr"},
    533: {"name": "Mensa HfS Schnellerstraße", "command": "hfs_schnellerstr"},
    320: {"name": "Mensa HTW Treskowallee", "command": "htw_treskowallee"},
    319: {"name": "Mensa HTW Wilhelminenhof", "command": "htw_wilhelminenhof"},
    147: {"name": "Mensa HU Nord", "command": "hu_nord"},
    191: {"name": "Mensa HU Oase Adlershof", "command": "hu_adlershof"},
    367: {"name": "Mensa HU Süd", "command": "hu_sued"},
    270: {"name": "Mensa HU Spandauer Straße", "command": "hu_spandauer"},
    526: {"name": "Mensa HWR Badensche Straße", "command": "hwr_badenschestr"},
    532: {"name": "Mensa Katholische HS für Sozialwesen", "command": "khs_mensa"},
    530: {"name": "Mensa KHS Weißensee", "command": "khs_weissensee"},
    321: {"name": "Mensa TU Hardenbergstraße", "command": "tu_mensa"},
    323: {"name": "Mensa Veggie N° 1 - Die grüne Mensa", "command": "fu_veggie"},
    368: {"name": "Cafeteria FU Ihnestraße", "command": "fu_ihnestr"},
    660: {"name": "Cafeteria FU Koserstraße", "command": "fu_koserstr"},
    542: {"name": "Cafeteria FU Pharmazie", "command": "fu_pharmazie"},
    277: {"name": "Cafeteria FU Rechtswissenschaft", "command": "fu_rechtswissenschaft"},
    543: {"name": "Cafeteria FU Wirtschaftswissenschaften", "command": "fu_wirtschaftswissenschaften"},
    726: {"name": "Cafeteria HTW Treskowallee", "command": "htw_treskowallee_cafeteria"},
    659: {"name": "Cafeteria HU „Jacob und Wilhelm Grimm Zentrum“", "command": "hu_wilhelm_grimm_zentrum"},
    539: {"name": "Cafeteria TU Ackerstraße", "command": "tu_ackerstr"},
    540: {"name": "Cafeteria TU Architektur", "command": "tu_architektur"},
    657: {"name": "Cafeteria TU „Skyline“", "command": "tu_skyline"},
    631: {"name": "Cafeteria TU Hardenbergstraße", "command": "tu_mensa_cafeteria"},
    541: {"name": "Cafeteria TU Hauptgebäude „Wetterleuchten“", "command": "tu_wetterleuchten"},
    538: {"name": "Cafeteria TU Marchstraße", "command": "tu_marchstr"},
    722: {"name": "Cafeteria UdK „Jazz-Cafe“", "command": "udk_jazz_cafe"},
    658: {"name": "Cafeteria UdK Lietzenburger Straße", "command": "udk_lietzenburgerstr"},
    647: {"name": "Coffeebar Beuth Hochschule", "command": "beuth_coffeebar"},
    648: {"name": "Coffeebar Beuth Hochschule Haus Grashof", "command": "beuth_coffeebar_haus_grashof"},
    1407: {"name": "Coffeebar EHB Teltower Damm", "command": "ehb_teltower_damm_coffeebar"},
    723: {"name": "Coffeebar HfM „Neuer Marstall“", "command": "hfm_neuer_marstall"},
    724: {"name": "Coffeebar HfM Charlottenstraße", "command": "hfm_charlottenstr_coffeebar"},
    725: {"name": "Coffeebar HTW Wilhelminenhof", "command": "htw_wilhelminenhof_coffeebar"},
    661: {"name": "Coffeebar HU „c.t“", "command": "hu_ct"},
    721: {"name": "Coffeebar HU Mensa Nord", "command": "hu_nord_coffeebar"},
    720: {"name": "Coffeebar HU Oase Adlershof", "command": "hu_adlershof_coffeebar"},
    727: {"name": "Coffeebar HWR Alt-Friedrichsfelde", "command": "hwr_alt_friedrichsfelde"},
    728: {"name": "Coffeebar HWR Badensche Straße", "command": "hwr_badenschestr_coffeebar"},
    649: {"name": "Coffeebar Mensa FU II", "command": "fu_2_coffeebar"},
    650: {"name": "Coffeebar Mensa Lankwitz", "command": "fu_lankwitz_coffeebar"},
    632: {"name": "Coffeebar TU Hardenbergstraße", "command": "tu_mensa_coffeebar"},
}


def fetch_POST(url, data):
    data = urllib.parse.urlencode(data)
    data = data.encode('ascii')

    # a user agent is required by server (TODO: fake_useragent?)
    headers = {'User-Agent': "Mozilla/5.0 (compatible)"}

    req = urllib.request.Request(url, data, headers=headers)
    with urllib.request.urlopen(req) as f:
        return BeautifulSoup(f.read().decode('utf-8'), 'html.parser')


def parse_day(canteen, url, date, data):
    data.update({'date': date.isoformat()})
    soup = fetch_POST(url, data)

    categories = soup.find_all('div', class_='splGroupWrapper')
    # check if cafeteria is closed
    # assume_closed and is necessary b/c of category_name
    if len(categories) == 1 and categories[0].find('div') is None and categories[0].find('br').text.strip() == 'Kein Speisenangebot':
        canteen.setDayClosed(date)
    else:
        priced_items = False
        for category in categories:
            category_name = category.find('div', class_='splGroup').text.strip()
            meals = soup.find_all('div', class_='splMeal')
            for meal in meals:
                name = meal.find('span', class_='bold').text.strip()
                prices = meal.find('div', class_='text-right').text.strip().split('/')
                if len(prices) == 1:
                    if prices[0] == '':
                        prices = None
                    else:
                        prices = len(roles) * [prices[0]]
                if prices:
                    priced_items = True
                    prices = buildPrices(prices, roles)

                notes = []

                imgs = meal.find_all('img', class_='splIcon')
                for img in imgs:
                    src = img.attrs['src']
                    src = src.rsplit('/', 1)[-1]
                    if src in img_map:
                        notes.append(img_map[src])

                notes.extend([td.text.strip() for td in meal.find('div', class_='kennz').find_all('td', class_=None)])

                canteen.addMeal(date, category_name, name, notes, prices)

        # check there is at least one price tag per day, otherwise assume
        # closed b/c some cafererias serve salat dressings etc. on closed days
        if not priced_items:
            canteen.setDayClosed(date)


def parse_url(url, today=False, **data):
    canteen = BaseBuilder()

    date = datetime.date.today()
    # data is provided for either current and next week or for today only
    days = 2 * 7 - date.isoweekday() + 1
    if today:
        days = 1

    while days > 0:
        parse_day(canteen, url, date, data)
        date += datetime.timedelta(days=1)
        days -= 1

    return canteen.toXMLFeed()


parser = Parser('berlin', handler=parse_url,
                shared_prefix='https://www.stw.berlin/xhr/speiseplan-wochentag.html')
for (k, v) in mapping.items():
    parser.define("{}".format(v['command']), '', extra_args={'resources_id': k})

# for debugging / testing
if __name__ == "__main__":
    print(parser.parse("berlin", "tu_mensa", 'today.xml'))
