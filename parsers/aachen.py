from collections import OrderedDict
import re
from urllib import request

from bs4 import BeautifulSoup as fetch_url
from bs4.element import Tag

from model.model_helpers import NotesBuilder, PricesBuilder, PricesCategoryBuilder
from model.openmensa_model import Canteen, Category, ClosedDay, Day, Meal, Prices
from pyopenmensa.feed import buildLegend, convertPrice, extractDate
from utils import Parser


def parse_url(url, today=False):
    document = fetch_url(request.urlopen(url).read(), 'lxml')

    return parse(document)


def parse(document):
    legend = parse_legend(document.find(id='additives'))
    all_days = parse_all_days(document, legend)
    canteen = Canteen(all_days)
    return canteen.to_string()


def parse_legend(legend_container):
    regex = r'\((?P<name>[\dA-Z]+)\) (enthält eine )?(?P<value>[\wäöüß\s]+)'
    return buildLegend(text=legend_container.text, regex=regex)


def parse_all_days(document, legend):
    days = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
            'MontagNaechste', 'DienstagNaechste', 'MittwochNaechste',
            'DonnerstagNaechste', 'FreitagNaechste')

    all_days = []
    for day in days:
        day_container = document.find('div', id=day)
        if day_container is None:
            continue
        day = parse_day(day_container, legend)
        all_days.append(day)

    return all_days


def parse_day(day_container, legend):
    date_description = day_container.find_previous_sibling('h3')
    date = extractDate(date_description.text)

    if is_closed(day_container):
        return ClosedDay(date)

    meals_table = day_container.find(attrs={'class': 'menues'})
    menues = parse_categories(meals_table, legend)

    extras_table = day_container.find(attrs={'class': 'extras'})
    extras = parse_categories(extras_table, legend)

    all_categories = menues + extras
    if len(all_categories) == 0:
        return ClosedDay(date)
    else:
        return Day(date, all_categories)


def is_closed(data):
    note = data.find(id='note')
    if note:
        return True
    else:
        return False


def parse_categories(categories_container, legend):
    category_dict = OrderedDict()
    for meal_entry in categories_container.find_all('tr'):
        category_name = meal_entry.find('span', attrs={'class': 'menue-category'}).text.strip()
        meal = parse_meal_entry(meal_entry, legend)

        if category_name and meal:
            category_dict.setdefault(category_name, []).append(meal)

    subsidized_categories = [
        'Tellergericht',
        'Vegetarisch',
        'Klassiker',
        'Empfehlung des Tages'
    ]
    supplements = PricesBuilder(student=0, other=150)

    all_categories = []
    for category_name, meals in category_dict.items():
        if category_name in subsidized_categories and meals[0].prices:
            default_price = meals[0].prices.prices['other']
            category_builder = PricesCategoryBuilder(
                supplements.build_prices(default_price),
                overwrite_existing=True
            )
            category = category_builder.build_category(category_name, meals)
        else:
            category = Category(category_name, meals)
        all_categories.append(category)

    return all_categories


def parse_meal_entry(meal_entry, legend):
    description_container = meal_entry.find('span', attrs={'class': 'menue-desc'})
    clean_description_container = extract_description_element(description_container)
    name, note_keys = extract_name_and_note_keys(clean_description_container)
    notes_builder = NotesBuilder(legend)
    notes = notes_builder.build_notes(note_keys)

    price_tag = meal_entry.find('span', attrs={'class': 'menue-price'})
    prices = None
    if price_tag:
        price_tag = convertPrice(price_tag.text.strip())
        prices = Prices(other=price_tag)

    meal = None
    if name and not re.search(r'^geschlossen|ausverkauft|kein \S*angebot', name, re.IGNORECASE):
        meal = Meal(name, prices=prices, notes=notes)

    return meal


def extract_description_element(description_container):
    # "Hauptbeilage" and "Nebenbeilage" are flat,
    # while the others are wrapped in <span class="expand-nutr">
    effective_description_container = description_container.find('span', attrs={
        'class': 'expand-nutr'
    }) or description_container

    def is_valid_description_element(element):
        if not isinstance(element, Tag):
            return True
        # Keep <span class="seperator">oder</span>, notice typo in "seperator"
        if element.name == 'span' and 'seperator' in element['class']:
            # Sometimes it's empty, i. e. <span class="seperator"></span>
            return len(element.contents) > 0
        # Keep <sup> tags for notes
        if element.name == 'sup':
            return True
        return False

    description_container = list(filter(
        is_valid_description_element,
        effective_description_container.children
    ))

    return description_container


def extract_name_and_note_keys(description_container):
    name_parts = []
    note_keys = set()
    for element in description_container:
        if type(element) is Tag and element.name == 'sup':
            new_note_keys = element.text.strip().split(',')
            note_keys.update(new_note_keys)
        else:
            name_parts.append(element.string)
    note_keys.discard('')
    raw_name = ' '.join(name_parts)
    # Remove redundant as well as leading and trailing whitespace:
    name = re.sub(r"\s+", ' ', raw_name).strip()
    return name, list(note_keys)


parser = Parser(
    'aachen',
    handler=parse_url,
    shared_prefix='http://www.studierendenwerk-aachen.de/speiseplaene/',
)

parser.define('academica', suffix='academica-w.html')
parser.define('ahorn', suffix='ahornstrasse-w.html')
parser.define('templergraben', suffix='templergraben-w.html')
parser.define('bayernallee', suffix='bayernallee-w.html')
parser.define('eups', suffix='eupenerstrasse-w.html')
parser.define('goethe', suffix='goethestrasse-w.html')
parser.define('vita', suffix='vita-w.html')
parser.define('zeltmensa', suffix='forum-w.html')
parser.define('juelich', suffix='juelich-w.html')
