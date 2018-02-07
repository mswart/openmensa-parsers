import copy
import re
from urllib import request

from bs4 import BeautifulSoup as parse, NavigableString

import openmensa_model as OpenMensa
from parsers.aachen.utils import OrderedCounter
from pyopenmensa.feed import buildLegend, convertPrice, extractDate
from utils import Parser
from . import model as Aachen


def parse_url(url, today=False):
    raw_this_week_html = request.urlopen(url + '_diese_woche.html').read()
    raw_next_week_html = request.urlopen(url + '_naechste_woche.html').read()

    document_this_week = parse(raw_this_week_html, 'lxml')
    document_next_week = parse(raw_next_week_html, 'lxml')

    this_week_days = parse_document(document_this_week)
    next_week_days = parse_document(document_next_week)
    all_days = this_week_days + next_week_days

    legend = parse_legend(document_this_week)
    feed = convert_to_openmensa_feed(all_days, legend)
    return feed.to_string()


def parse_legend(legend_container):
    legend_div = legend_container.find(attrs={'class': 'bottom-wrap'})
    additive_container, allergens = legend_div.find_all('div')

    raw_legend_string = additive_container.text + allergens.text
    regex = r'\((?P<name>[\dA-Z]+)\) (?P<value>[\wäüöÄÜÖß ]+)'
    return buildLegend(text=raw_legend_string, regex=regex)


def parse_document(document):
    table = document.find(attrs={'class': 'dc-wrap'}).table

    category_counter = OrderedCounter(parse_categories(table))

    day_columns = transpose_table_to_day_columns(table)
    all_days = [parse_day(category_counter, column) for column in day_columns]
    return all_days


def parse_categories(category_container):
    table_rows = category_container.find_all('tr')
    # Get first cell of all rows, excluding header row
    category_table_cells = [row.find('td') for row in table_rows[1:]]

    categories = [
        parse_category(cell) for cell in category_table_cells
    ]
    return categories


def parse_category(category_cell):
    if len(category_cell.contents) == 3:  # <td>Klassiker <br> 2,60€</td>
        category_name, price = parse_main_category(category_cell)
    else:  # <td>Nebenbeilage</td>
        category_name, price = parse_side_category(category_cell)

    return Aachen.Category(category_name, price)


def parse_main_category(category_cell):
    category_name_element, _, price_string_element = category_cell.children
    category_name = str(category_name_element)

    price_string = str(price_string_element)
    price = convertPrice(price_string)
    # Subsidized categories
    if category_name in ['Tellergericht', 'Vegetarisch', 'Empfehlung des Tages', 'Klassiker',
                         'Süßspeise']:
        subsidized_roles = [Aachen.Role('student'), Aachen.Role('other', 150)]
        price = Aachen.PriceWithRoles(price, subsidized_roles)

    return category_name, price


def parse_side_category(category_cell):
    category_name = str(category_cell.text)
    price = None

    return category_name, price


def transpose_table_to_day_columns(table):
    return [
        [row.contents[column_index] for row in table.find_all('tr')]
        for column_index in range(1, 6)
    ]


def parse_day(category_counter, day_column):
    categories = extract_categories(category_counter, day_column)

    day_date_string = day_column[0].text
    date = extractDate(day_date_string)

    if all(map(is_empty_category, categories)):
        return OpenMensa.DayClosed(date)
    else:
        return OpenMensa.Day(date, categories)


def is_empty_category(category):
    return len(category.meals) == 0


def extract_categories(category_counter, day_column):
    row_counter = 1
    categories = []
    for (template_category, occurrences) in category_counter.items():
        category = copy.deepcopy(template_category)
        for meal_number in range(occurrences):
            meal = parse_meal(day_column[row_counter])
            if meal:
                category.append(meal)

            row_counter += 1

        if not is_empty_category(category):
            categories.append(category)
    return categories


def parse_meal(meal_container):
    if 'main-dish' in meal_container.parent['class']:
        description_container = meal_container.find('p', attrs={'class': 'dish-text'})
    elif 'side-dish' in meal_container.parent['class']:
        description_container = meal_container
    else:
        raise ValueError("Element {} should have a parent with either the `main-dish` "
                         "or `side-dish` class.".format(meal_container))

    if description_container and description_container.text:
        return parse_meal_description(description_container)
    else:
        return None


def parse_meal_description(description_container):
    raw_description = get_description(description_container)

    if re.search(r'((heute )?kein (\w)*angebot|geschlossen)', raw_description, re.IGNORECASE):
        return None

    all_note_keys, description_without_notes = extract_note_keys(description_container,
                                                                 raw_description)

    return Aachen.Meal(description_without_notes, all_note_keys)


def get_description(description_container):
    description_elements = description_container.contents
    description_string_parts = [element.string for element in description_elements
                                if isinstance(element, NavigableString)]
    # Clean leading and trailing whitespace
    description_string_parts = list(map(
        lambda string: re.sub(r'(^\s+|\s+$)', '', string),
        description_string_parts
    ))
    # Clean redundant whitespace
    description_string_parts = list(map(
        lambda string: re.sub(r'\s+', ' ', string),
        description_string_parts
    ))
    raw_description = ' | '.join(description_string_parts)
    return raw_description


def extract_note_keys(description_container, raw_description):
    note_regex = re.compile(r' \(((?:[A-Z\d]+,?)+)\)')

    all_note_keys = set()
    for match in note_regex.finditer(raw_description):
        note_group = match.group(1)
        note_keys = note_group.split(',')
        all_note_keys.update(note_keys)

    if description_container.parent.find('img', attrs={'class': 'vegan'}) is not None:
        all_note_keys.add('vegan')

    # Remove notes from description
    cleaned_description = note_regex.sub('', raw_description)

    return all_note_keys, cleaned_description


def convert_to_openmensa_feed(all_days, legend):
    feed = OpenMensa.Canteen()
    for day in all_days:
        if isinstance(day, OpenMensa.DayClosed):
            feed.insert(OpenMensa.DayClosed(day.date))
        else:
            openmensa_day = OpenMensa.Day(day.date)
            for category in day.categories:
                openmensa_category = OpenMensa.Category(category.name)
                for meal in category.meals:
                    notes = list(
                        map(lambda note_key: legend[note_key] if note_key in legend else note_key,
                            meal.note_keys)
                    )
                    if category.price is None:
                        prices = []
                    elif isinstance(category.price, Aachen.PriceWithRoles):
                        prices = [
                            OpenMensa.Price(category.price.base_price + role.surcharge, role.name)
                            for role in category.price.roles
                        ]
                    elif isinstance(category.price, int):
                        prices = [OpenMensa.Price(category.price)]
                    else:
                        raise TypeError("Unknown type {} for price {}.".format(type(category.price),
                                                                               category.price))
                    openmensa_meal = OpenMensa.Meal(meal.name, prices=prices, notes=notes)
                    openmensa_category.append(openmensa_meal)

                openmensa_day.append(openmensa_category)
            feed.insert(openmensa_day)
    return feed


parser = Parser(
    'aachen',
    handler=parse_url,
    shared_prefix='http://www.studierendenwerk-aachen.de/files/content/Downloads/Gastronomie/Speiseplaene/speiseplan_mensa_'
)

parser.define('academica', suffix='academica')
parser.define('ahorn', suffix='ahornstrasse')
parser.define('templergraben', suffix='bistro_templergraben')
parser.define('bayernallee', suffix='bayernallee')
parser.define('eupenerstrasse', suffix='eupener_strasse')
parser.define('goethestrasse', suffix='goethestrasse')
parser.define('vita', suffix='vita')
parser.define('suedpark', suffix='suedpark')
parser.define('juelich', suffix='juelich')
