import re
from urllib import request

from bs4 import BeautifulSoup as parse
from bs4.element import Tag

from model.model_helpers import NotesBuilder
from model.openmensa_model import Canteen, Category, ClosedDay, Day, Meal, Prices
from pyopenmensa.feed import buildLegend, convertPrice, extractDate
from utils import Parser


def parse_url(url, today=False):
    document = parse(request.urlopen(url).read(), 'lxml')

    legend = AachenParser.parse_legend(document.find(id='additives'))
    parser = AachenParser(legend)

    return parser.parse(document)


class AachenParser:
    def __init__(self, legend):
        self.legend = legend

    @staticmethod
    def parse_legend(legend_container):
        regex = '\((?P<name>[\dA-Z]+)\) (enthält eine )?(?P<value>[\wäöüß\s]+)'
        return buildLegend(text=legend_container.text, regex=regex)

    def parse(self, document):
        all_days = self.parse_all_days(document)
        canteen = Canteen(all_days)
        return canteen.to_string()

    def parse_all_days(self, document):
        days = ('Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
                'MontagNaechste', 'DienstagNaechste', 'MittwochNaechste', 'DonnerstagNaechste',
                'FreitagNaechste')
        all_days = []
        for day in days:
            day_container = document.find('div', id=day)
            if day_container is None:
                continue
            day = self.parse_day(day_container)
            all_days.append(day)
        return all_days

    def parse_day(self, day_container):
        day = day_container.find_previous_sibling('h3')
        date = extractDate(day.text)
        if self.is_closed(day_container):
            return ClosedDay(date)

        meals_table = day_container.find(attrs={'class': 'menues'})
        menues = self.parse_categories(meals_table)

        extras_table = day_container.find(attrs={'class': 'extras'})
        extras = self.parse_categories(extras_table)

        all_categories = [*menues, *extras]
        return Day(date, all_categories)

    def is_closed(self, data):
        note = data.find(id='note')
        if note:
            return True
        else:
            return False

    def parse_categories(self, categories_container):
        category_dict = {}
        for meal_entry in categories_container.find_all('tr'):
            category, price, meal = self.parse_meal(meal_entry)
            if category and meal:
                category_dict.setdefault(category, []).append(meal)

        all_categories = [Category(name, meals) for name, meals in category_dict.items()
                          if name and meals]
        return all_categories

    def parse_meal(self, table_row):
        category_name = table_row.find('span', attrs={'class': 'menue-category'}).text.strip()

        description_container = table_row.find('span', attrs={'class': 'menue-desc'})
        clean_description_container = self.get_cleaned_description_container(description_container)
        name, note_keys = self.parse_description(clean_description_container)
        notes_builder = NotesBuilder(self.legend)
        notes = notes_builder.build_notes(note_keys)

        price_tag = table_row.find('span', attrs={'class': 'menue-price'})
        prices = None
        if price_tag:
            price_tag = convertPrice(price_tag.text.strip())
            prices = Prices(student=price_tag, other=price_tag + 150)

        meal = None
        if name:
            meal = Meal(name, prices=prices, notes=notes)

        return category_name, price_tag, meal

    def get_cleaned_description_container(self, description_container):
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

    def parse_description(self, description_container):
        name_parts = []
        note_keys = set()
        for element in description_container:
            if type(element) is Tag and element.name == 'sup':
                new_note_keys = element.text.strip().split(',')
                note_keys.update(new_note_keys)
            else:
                name_parts.append(element.string.strip())
        name = re.sub(r"\s+", ' ', ' '.join(name_parts))
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
