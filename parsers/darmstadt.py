#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup

from utils import Parser

legend_tag_regex = r'\((?P<name>(\d|[a-zA-Z])+)\)\s*' + \
                   r'(?P<value>\w+((\s+\w+)*[^0-9)]))'
# FIXME: legend value ending with (bracketed word) miss it


def parse_week(url, canteen):
    soup = BeautifulSoup(urlopen(url).read(), 'html.parser')

    # TODO: vegetarisch, vegan, Schwein, ... -- indicated via inline SVGs only
    # legend is a .jpg nowadays, fill it manually
    canteen.setLegendData(text="""
        (A) Glutenhaltiges Getreide
        (B) Krebstiere und Krebstiererzeugnisse
        (C) Eier und Eierzeugnisse
        (D) Fisch und Fischerzeugnisse
        (E) Erdnüsse und Erdnusserzeugnisse
        (F) Soja und Sojaerzeugnisse
        (G) Milch und Milcherzeugnisse
        (H) Schalenfrüchte
        (I) Sellerie und Sellerieerzeugnisse
        (J) Senf und Senferzeugnisse
        (K) Sesamsamen und Sesamsamenerzeugnisse
        (L) Schwefeldioxid und Sulfite
        (M) Lupine und Lupinenerzeugnisse
        (N) Weichtiere (Mollusken)
        (1) Lebensmittelfarbe
        (2) Konservierungsstoff
        (3) Antioxidationsmittel
        (4) Geschmacksverstärker
        (5) geschwefelt
        (6) geschwärzt
        (7) gewachst
        (8) Phosphat
        (9) Süßungsmittel
        (10) Phenylalaninquelle""",
                    legend=canteen.legendData,
                    regex=legend_tag_regex)

    # TODO: "geschlossen" - need sample how they do/break it
    for day_section in soup.find_all('section', {'class': 'fmc-day'}):
        date_tag = day_section.find('div', {'class': 'fmc-head'})
        if not date_tag:
            print("No date found in section " + day_section)
            continue

        date = ' '.join(date_tag.strings)

        for meal_item in day_section.find_all('li', {'class': 'fmc-item'}):
            title_tag = meal_item.find('span', {'class': 'fmc-item-title'})
            location_tag = meal_item.find('span', {'class': 'fmc-item-location'})
            price_tag = meal_item.find('span', {'class': 'fmc-item-price'})

            try:
                canteen.addMeal(date, category=location_tag.string,
                                name=title_tag.string,
                                prices=price_tag.string)
            except ValueError as e:
                print('Error adding meal "{}": {}'.format(meal_item, e))


def parse_url(url, today=False):
    canteen = LazyBuilder()
    canteen.setAdditionalCharges('student', {})
    parse_week(url, canteen)
    return canteen.toXMLFeed()


parser = Parser('darmstadt', handler=parse_url,
                shared_prefix='http://studierendenwerkdarmstadt.de/hochschulgastronomie/speisekarten/')
parser.define('stadtmitte', suffix='stadtmitte/')
parser.define('lichtwiese', suffix='lichtwiese/')
parser.define('schoefferstrasse', suffix='schoefferstrasse/')
parser.define('dieburg', suffix='dieburg/')
parser.define('haardtring', suffix='haardtring/')


# for debugging / testing
if __name__ == "__main__":
    print(parser.parse("darmstadt", "stadtmitte", None))
