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

    try:
        for legend_tag in soup.select('section.fmc-info p'):
            canteen.setLegendData(text=' '.join(legend_tag.strings),
                    legend=canteen.legendData,
                    regex=legend_tag_regex)
    except Exception as e:
        print('Error in parsing legend ' + str(e))

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
