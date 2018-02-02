import re
from urllib import request

from bs4 import BeautifulSoup as parse
from bs4.element import Tag

from parsers.aachen.canteen import Category, Day, DayClosed, Entry, Meal, Xml
from pyopenmensa.feed import buildLegend, extractDate, convertPrice
from utils import Parser


def parse_url(url, today=False):
    raw_this_week_html = request.urlopen(url + '_diese_woche.html').read()
    raw_next_week_html = request.urlopen(url + '_naechste_woche.html').read()

    document_this_week = parse(raw_this_week_html, 'lxml')
    document_next_week = parse(raw_next_week_html, 'lxml')

    this_week_days = parse_all_days(document_this_week)
    next_week_days = parse_all_days(document_next_week)

    all_days = this_week_days + next_week_days
    return parse_html_document(document_this_week, all_days)


def parse_html_document(legend_container, all_days):
    legend = parse_legend(legend_container)
    xml = Xml()
    feed_xml = xml.days_to_xml(all_days, legend, {'student': 0, 'other': 150})

    return xml.xml_to_string(feed_xml)


def parse_legend(legend_container):
    legend_div = legend_container.find(attrs={'class': 'bottom-wrap'})
    additive_container, allergens = legend_div.find_all('div')

    raw_legend_string = additive_container.text + allergens.text
    regex = '\((?P<name>[\dA-Z]+)\) (?P<value>[\wäüöÄÜÖß ]+)'
    return buildLegend(text=raw_legend_string, regex=regex)


def parse_all_days(document):
    days = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
            'MontagNaechste', 'DienstagNaechste', 'MittwochNaechste', 'DonnerstagNaechste',
            'FreitagNaechste')
    all_days = []
    for day in days:
        day_column = document.find('div', id=day)
        if day_column is None:  # assume closed?
            continue
        day = parse_day(day_column)
        all_days.append(day)

    return all_days


def parse_day(day_container):
    day_header = day_container.find_previous_sibling('h3')
    date_string = day_header.text
    date = extractDate(date_string)
    if is_closed(day_container):
        return DayClosed(date)

    meals_table = day_container.find(attrs={'class': 'menues'})
    meal_entries = parse_all_entries_from_table(meals_table)

    extras_table = day_container.find(attrs={'class': 'extras'})
    extras_entries = parse_all_entries_from_table(extras_table)

    all_entries = meal_entries + extras_entries

    day = Day(date)
    for entry in all_entries:
        try:
            day.parse_entry(entry)
        except ValueError as e:
            print("Ignored error on meal addition: " + str(e))

    return day


def is_closed(data):
    note = data.find(id='note')
    if note:
        return True
    else:
        return False


def parse_all_entries_from_table(table):
    all_entries = []
    for item in table.find_all('tr'):
        entry = parse_entry(item)
        all_entries.append(entry)

    return all_entries


def parse_entry(table_row):
    category = parse_category(table_row)

    meal = parse_meal(table_row)

    return Entry(category, meal)


def parse_category(category_container):
    category_name = category_container.find('span', attrs={'class': 'menue-category'}).text.strip()

    category = Category(category_name)

    return category


def parse_meal(meal_container):
    description_container = meal_container.find('span', attrs={'class': 'menue-desc'})
    clean_description_container = get_cleaned_description_container(description_container)

    name_parts = []
    notes = set()

    for element in clean_description_container:
        if type(element) is Tag and element.name == 'sup':
            note = element.text.strip().split(',')
            if not note == ['']:
                notes.update(element.text.strip().split(','))
        else:
            name_parts.append(element.string.strip())
    name = re.sub(r"\s+", ' ', ' '.join(name_parts))

    meal = Meal(name)
    meal.note_keys = notes

    price_element = meal_container.find('span', attrs={'class': 'menue-price'})
    if price_element:
        price_string = price_element.text.strip()
        meal.price = convertPrice(price_string)

    return meal


def get_cleaned_description_container(meal_container):
    # "Hauptbeilage" and "Nebenbeilage" are flat,
    # while the others are wrapped in <span class="expand-nutr">
    effective_meal_container = meal_container.find('span', attrs={
        'class': 'expand-nutr'}) or meal_container

    def is_valid_meal_element(element):
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

    meal_container = list(filter(
        is_valid_meal_element,
        effective_meal_container.children
    ))

    return meal_container


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