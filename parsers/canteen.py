from collections import OrderedDict

import lxml.etree as ET


class Day:
    def __init__(self, date):
        self.date = date
        self.categories = OrderedDict()

    def parse_entry(self, entry):
        if entry.category.name not in self.categories:
            self.categories[entry.category.name] = entry.category

        try:
            self.categories[entry.category.name].add_meal(entry.meal)
        except ValueError as e:
            print("Ignored error on meal addition: " + str(e))


class DayClosed:
    def __init__(self, date):
        self.date = date


class Entry:
    def __init__(self, category, meal):
        self.category = category
        self.meal = meal


class Category:
    def __init__(self, name):
        self.name = name
        self.meals = []

    def add_meal(self, meal):
        if meal.name:
            self.meals.append(meal)
        else:
            raise ValueError("The meal ({}) had a missing name. "
                             "The meal was not added to this category ({}).".format(meal, self))


class Meal:
    def __init__(self, name, note_keys=None, price=None):
        """
        :type name: str
        """
        self.name = name
        self.note_keys = note_keys or []
        self.price = price


class Xml:
    def xml_to_string(self, xml, pretty_print=True):
        return ET.tostring(xml, encoding='UTF-8', xml_declaration=True, pretty_print=pretty_print).decode('utf-8')

    def days_to_xml(self, days, note_legend, price_roles):
        xmlns = 'http://openmensa.org/open-mensa-v2'
        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        schemaLocation = 'http://openmensa.org/open-mensa-v2.xsd'
        openmensa = ET.Element(
            'openmensa',
            attrib={
                'version': '2.1',
                "{" + xsi + "}schemaLocation": " ".join([xmlns, schemaLocation])
            },
            nsmap={None: xmlns, 'xsi': xsi}
        )
        canteen = ET.SubElement(openmensa, 'canteen')
        day_elements = [self.day_to_xml(day, note_legend, price_roles) for day in days]
        canteen.extend(day_elements)

        return openmensa

    def day_to_xml(self, day, note_legend, price_roles):
        day_element = ET.Element('day', {'date': day.date.isoformat()})

        if isinstance(day, DayClosed):
            closed = ET.SubElement(day_element, 'closed')
        else:
            category_elements = [
                self.category_to_xml(category, note_legend, price_roles)
                for category in day.categories.values()
            ]
            day_element.extend(category_elements)
        return day_element

    def category_to_xml(self, category, note_legend, price_roles):
        category_element = ET.Element('category', {'name': category.name})
        meal_elements = [self.meal_to_xml(meal, note_legend, price_roles) for meal in category.meals]
        category_element.extend(meal_elements)
        return category_element

    def meal_to_xml(self, meal, note_legend, price_roles):
        meal_element = ET.Element('meal')
        name = ET.SubElement(meal_element, 'name')
        name.text = meal.name

        notes = map(lambda key: note_legend[key] if key in note_legend else key, meal.note_keys)
        for note in sorted(notes):
            note_element = ET.SubElement(meal_element, 'note')
            note_element.text = note

        if meal.price:
            for role in sorted(price_roles):
                price = ET.SubElement(meal_element, 'price', {'role': role})
                role_price = meal.price + price_roles[role]
                price.text = "{:0,.2f}".format(role_price / 100)

        return meal_element
