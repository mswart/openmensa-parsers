import copy
import re
from urllib import request

from bs4 import BeautifulSoup as parse, NavigableString

from pyopenmensa.feed import buildLegend, extractDate
from utils import Parser
from . import model as Aachen
from . import openmensa_model as OpenMensa


def parse_url(url, today=False):
    raw_this_week_html = request.urlopen(url + '_diese_woche.html').read()
    raw_next_week_html = request.urlopen(url + '_naechste_woche.html').read()

    document_this_week = parse(raw_this_week_html, 'lxml')
    document_next_week = parse(raw_next_week_html, 'lxml')

    this_week_days = parse_document(document_this_week)
    next_week_days = parse_document(document_next_week)
    all_days = this_week_days + next_week_days

    legend = parse_legend(document_this_week)
    feed = convert_to_openmensa_model(all_days, legend)
    return feed.to_string()


def parse_legend(legend_container):
    legend_div = legend_container.find(attrs={'class': 'bottom-wrap'})
    additive_container, allergens = legend_div.find_all('div')

    raw_legend_string = additive_container.text + allergens.text
    regex = r'\((?P<name>[\dA-Z]+)\) (?P<value>[\wäüöÄÜÖß ]+)'
    return buildLegend(text=raw_legend_string, regex=regex)


def parse_document(document):
    table = document.find(attrs={'class': 'dc-wrap'}).table

    subsidized_roles = [OpenMensa.Role('student'), OpenMensa.Role('other', 150)]
    # Differentiate between categories with only one vs multiple rows in the table.
    categories_with_occurrences = [
        Aachen.Category('Tellergericht', price=OpenMensa.PriceWithRoles(180, subsidized_roles)),
        Aachen.Category('Vegetarisch', price=OpenMensa.PriceWithRoles(210, subsidized_roles)),
        Aachen.Category('Empfehlung des Tages',
                        price=OpenMensa.PriceWithRoles(390, subsidized_roles)),
        Aachen.Category('Klassiker', price=OpenMensa.PriceWithRoles(260, subsidized_roles)),
        Aachen.Category('Süßspeise', price=OpenMensa.PriceWithRoles(150, subsidized_roles)),
        Aachen.Category('Hauptbeilage'),
        Aachen.Category('Nebenbeilage'),
        Aachen.Category('Pizza des Tages', price=350),
        Aachen.Category('Burger des Tages', price=470),
        (Aachen.Category('Burger Classics', price=430), 4),
        Aachen.Category('Fingerfood', price=350),
        Aachen.Category('Sandwich', price=320),
        Aachen.Category('Flammengrill', price=450),
        (Aachen.Category('Wok', price=320), 2),
        (Aachen.Category('Pasta', price=350), 3),
    ]
    # Normalize so that all entries indicate the number of occurrences.
    categories_with_occurrences = list(
        map(lambda entry: (entry, 1) if isinstance(entry, Aachen.Category) else entry,
            categories_with_occurrences))

    day_columns = map_table_to_day_columns(table)
    all_days = [parse_day(categories_with_occurrences, column) for column in day_columns]
    return all_days


def map_table_to_day_columns(table):
    return [
        [row.contents[day_number] for row in table.find_all('tr')]
        for day_number in range(1, 6)
    ]


def parse_day(categories_with_occurrences, day_column):
    day_date_string = day_column[0].text
    date = extractDate(day_date_string)
    day = OpenMensa.Day(date)

    row_counter = 1
    for (template_category, occurrences) in categories_with_occurrences:
        category = copy.deepcopy(template_category)
        for meal_number in range(occurrences):
            try:
                meal = parse_meal(day_column[row_counter], category)
                category.append(meal)
            except LookupError:
                pass
            row_counter += 1

        if len(category.meals) > 0:
            day.append(category)

    return day


def parse_meal(meal_container, category):
    if category.name in ['Hauptbeilage', 'Nebenbeilage']:
        description_container = meal_container
    else:
        description_container = meal_container.find('p', attrs={'class': 'dish-text'})

    if description_container and description_container.text:
        description_elements = description_container.contents
        description_string_parts = [element.string for element in description_elements
                                    if isinstance(element, NavigableString)]
        # Some parts have leading and trailing whitespace
        description_string_parts = list(map(
            lambda string: re.sub(r'(^ | $)', '', string),
            description_string_parts
        ))
        raw_description = ' | '.join(description_string_parts)

        note_regex = re.compile(r' \(((?:[A-Z\d]+,?)+)\)')
        all_note_keys = set()
        for match in note_regex.finditer(raw_description):
            note_group = match.group(1)
            note_keys = note_group.split(',')
            all_note_keys.update(note_keys)

        if meal_container.find('img', attrs={'class': 'vegan'}) is not None:
            all_note_keys.add('vegan')

        cleaned_description = note_regex.sub('', raw_description)

        return Aachen.Meal(cleaned_description, all_note_keys)
    else:
        raise LookupError("No meal could be found in {}.".format(meal_container))


def convert_to_openmensa_model(all_days, legend):
    feed = OpenMensa.Canteen()
    for day in all_days:
        openmensa_day = OpenMensa.Day(day.date)
        for category in day.categories:
            openmensa_category = OpenMensa.Category(category.name)
            for meal in category.meals:
                notes = list(
                    map(lambda note_key: legend[note_key] if note_key in legend else note_key,
                        meal.note_keys))
                openmensa_meal = OpenMensa.Meal(meal.name, price=category.price, notes=notes)
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
