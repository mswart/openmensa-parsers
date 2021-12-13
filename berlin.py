#!/usr/bin/env python3

import datetime
import re
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from pyopenmensa.feed import LazyBuilder
from bs4 import BeautifulSoup
from utils import Parser


def parse_week(url, params, canteen):
    request = Request(url, data=urlencode(params).encode(), headers={
        'User-Agent': 'OpenMensa'})  # Python-urllib is blocked
    response = urlopen(request)
    soup = BeautifulSoup(response.read(), 'html.parser')

    date = soup.find('div', class_='col-xs-12').text.strip()
    # parsing code adapted from
    # <https://github.com/ekeih/OmNomNom/blob/master/canteens/studierendenwerk.py>
    for group in soup.find_all('div', class_='splGroupWrapper'):
        group_name = group.find('div', class_='splGroup')
        if not group_name:
            continue
        group_name = group_name.text.strip()
        for item in group.find_all('div', class_='splMeal'):
            title = item.find('span', class_='bold').text.strip()
            price_tag = item.find('div', class_='text-right').text.strip()
            prices = re.split(r'[^0-9,]+', price_tag)[1:4]
            notes = [td.text.strip() for td in
                     item.find_all('td', class_=False)]
            for icon in item.find_all('img', class_='splIcon'):
                if 'icons/15.png' in icon.attrs['src']:
                    notes.append("vegan")
                elif 'icons/43.png' in icon.attrs['src']:
                    notes.append("Klimaessen")
                elif 'icons/1.png' in icon.attrs['src']:
                    notes.append("Fisch- und Fleischfrei")
                elif 'icons/38.png' in icon.attrs['src']:
                    notes.append("MSC-Fisch")
                elif 'icons/18.png' in icon.attrs['src']:
                    notes.append("Bio")
            canteen.addMeal(date, category=group_name, name=title, notes=notes,
                            prices=prices,
                            roles=["student", "employee", "other"])


def parse_url(url, today=True, resources_id=0):
    canteen = LazyBuilder()
    days = [0] if today else range(-7, +28)
    for i in days:
        day = datetime.date.today() + datetime.timedelta(days=i)
        parse_week(url,
                   {"date": day.isoformat(), "resources_id": resources_id},
                   canteen)

    return canteen.toXMLFeed()


# canteen IDs and descriptions from
# <https://github.com/ekeih/OmNomNom/blob/master/canteens/studierendenwerk.py>
mapping = {
    534: {"description": "Mensa ASH Berlin Hellersdorf", "name": "ash_hellersdorf"},
    535: {"description": "Mensa Beuth Hochschule für Technik Kurfürstenstraße", "name": "beuth_kurfuerstenstr"},
    527: {"description": "Mensa Beuth Hochschule für Technik Luxemburger Straße", "name": "beuth_luxembugerstr"},
    537: {"description": "Mensa Charité Zahnklinik", "name": "charite_zahnklinik"},
    529: {"description": "Mensa EHB Teltower Damm", "name": "ehb_teltower_damm"},
    271: {"description": "Mensa FU Herrenhaus Düppel", "name": "fu_dueppel"},
    322: {"description": "Mensa FU II Otto-von-Simson-Straße", "name": "fu_2"},
    528: {"description": "Mensa FU Lankwitz Malteserstraße", "name": "fu_lankwitz"},
    531: {"description": "Mensa HfM Charlottenstraße", "name": "hfm_charlottenstr"},
    533: {"description": "Mensa HfS Schnellerstraße", "name": "hfs_schnellerstr"},
    320: {"description": "Mensa HTW Treskowallee", "name": "htw_treskowallee"},
    319: {"description": "Mensa HTW Wilhelminenhof", "name": "htw_wilhelminenhof"},
    147: {"description": "Mensa HU Nord", "name": "hu_nord"},
    191: {"description": "Mensa HU Oase Adlershof", "name": "hu_adlershof"},
    367: {"description": "Mensa HU Süd", "name": "hu_sued"},
    270: {"description": "Mensa HU Spandauer Straße", "name": "hu_spandauer"},
    526: {"description": "Mensa HWR Badensche Straße", "name": "hwr_badenschestr"},
    532: {"description": "Mensa Katholische HS für Sozialwesen", "name": "khs_mensa"},
    530: {"description": "Mensa KHS Weißensee", "name": "khs_weissensee"},
    321: {"description": "Mensa TU Hardenbergstraße", "name": "tu_mensa"},
    323: {"description": "Mensa Veggie N° 1 - Die grüne Mensa", "name": "fu_veggie"},
    368: {"description": "Cafeteria FU Ihnestraße", "name": "fu_ihnestr"},
    660: {"description": "Cafeteria FU Koserstraße", "name": "fu_koserstr"},
    542: {"description": "Cafeteria FU Pharmazie", "name": "fu_pharmazie"},
    277: {"description": "Cafeteria FU Rechtswissenschaft", "name": "fu_rechtswissenschaft"},
    543: {"description": "Cafeteria FU Wirtschaftswissenschaften", "name": "fu_wirtschaftswissenschaften"},
    726: {"description": "Cafeteria HTW Treskowallee", "name": "htw_treskowallee_cafeteria"},
    659: {"description": "Cafeteria HU „Jacob und Wilhelm Grimm Zentrum“", "name": "hu_wilhelm_grimm_zentrum"},
    539: {"description": "Cafeteria TU Ackerstraße", "name": "tu_ackerstr"},
    540: {"description": "Cafeteria TU Architektur", "name": "tu_architektur"},
    657: {"description": "Cafeteria TU „Skyline“", "name": "tu_skyline"},
    631: {"description": "Cafeteria TU Hardenbergstraße", "name": "tu_mensa_cafeteria"},
    541: {"description": "Cafeteria TU Hauptgebäude „Wetterleuchten“", "name": "tu_wetterleuchten"},
    538: {"description": "Cafeteria TU Marchstraße", "name": "tu_marchstr"},
    722: {"description": "Cafeteria UdK „Jazz-Cafe“", "name": "udk_jazz_cafe"},
    658: {"description": "Cafeteria UdK Lietzenburger Straße", "name": "udk_lietzenburgerstr"},
    647: {"description": "Coffeebar Beuth Hochschule", "name": "beuth_coffeebar"},
    648: {"description": "Coffeebar Beuth Hochschule Haus Grashof", "name": "beuth_coffeebar_haus_grashof"},
    1407: {"description": "Coffeebar EHB Teltower Damm", "name": "ehb_teltower_damm_coffeebar"},
    723: {"description": "Coffeebar HfM „Neuer Marstall“", "name": "hfm_neuer_marstall"},
    724: {"description": "Coffeebar HfM Charlottenstraße", "name": "hfm_charlottenstr_coffeebar"},
    725: {"description": "Coffeebar HTW Wilhelminenhof", "name": "htw_wilhelminenhof_coffeebar"},
    661: {"description": "Coffeebar HU „c.t“", "name": "hu_ct"},
    721: {"description": "Coffeebar HU Mensa Nord", "name": "hu_nord_coffeebar"},
    720: {"description": "Coffeebar HU Oase Adlershof", "name": "hu_adlershof_coffeebar"},
    727: {"description": "Coffeebar HWR Alt-Friedrichsfelde", "name": "hwr_alt_friedrichsfelde"},
    728: {"description": "Coffeebar HWR Badensche Straße", "name": "hwr_badenschestr_coffeebar"},
    649: {"description": "Coffeebar Mensa FU II", "name": "fu_2_coffeebar"},
    650: {"description": "Coffeebar Mensa Lankwitz", "name": "fu_lankwitz_coffeebar"},
    632: {"description": "Coffeebar TU Hardenbergstraße", "name": "tu_mensa_coffeebar"},
}

parser = Parser('berlin', handler=parse_url,
                shared_prefix='https://www.stw.berlin/xhr/speiseplan-wochentag.html')
for id, sub in mapping.items():
    parser.define(sub["name"], extra_args={'resources_id': id})

# for debugging / testing
if __name__ == "__main__":
    print(parser.parse("berlin", mapping[321]["name"], "today.xml"))
