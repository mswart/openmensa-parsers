from enum import Enum

import lxml.etree as ET


class Canteen:
    def __init__(self, days=None):
        self.days = days or []

    def insert(self, day):
        self.days.append(day)

    def to_string(self, pretty_print=True):
        return ET.tostring(self.to_xml(), encoding='UTF-8', xml_declaration=True,
                           pretty_print=pretty_print).decode('utf-8')

    def to_xml(self):
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
        day_elements = [day.to_xml() for day in self.days]
        canteen.extend(day_elements)

        return openmensa

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Day:
    def __init__(self, date, categories=None):
        self.date = date
        self.categories = categories or []

    def append(self, category):
        self.categories.append(category)

    def to_xml(self):
        day_element = ET.Element('day', {'date': self.date.isoformat()})
        category_elements = [category.to_xml() for category in self.categories]
        day_element.extend(category_elements)
        return day_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class ClosedDay:
    def __init__(self, date):
        self.date = date

    def to_xml(self):
        day_element = ET.Element('day', {'date': self.date.isoformat()})
        ET.SubElement(day_element, 'closed')
        return day_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Category:
    def __init__(self, name, meals=None):
        self.name = name
        self.meals = meals or []

    def append(self, meal):
        self.meals.append(meal)

    def to_xml(self):
        category_element = ET.Element('category', {'name': self.name})
        meal_elements = [meal.to_xml() for meal in self.meals]
        category_element.extend(meal_elements)
        return category_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Meal:
    def __init__(self, name, prices=None, notes=None):
        self.name = name
        self.prices = prices
        self.notes = notes or Notes()

    def to_xml(self):
        meal_element = ET.Element('meal')
        name = ET.SubElement(meal_element, 'name')
        name.text = self.name

        note_elements = self.notes.to_xml()
        meal_element.extend(note_elements)

        if self.prices:
            price_elements = self.prices.to_xml()
            meal_element.extend(price_elements)

        return meal_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Role(Enum):
    PUPILS = 'pupils'
    STUDENTS = 'students'
    EMPLOYEES = 'employees'
    OTHERS = 'other'


class Prices:
    def __init__(self, other=None, pupils=None, students=None, employees=None):
        if all(role is None for role in [other, pupils, students, employees]):
            raise ValueError("Prices awaits an amount for at least one of the roles "
                             "others, pupils, students or employees.")

        self.prices = {
            'other': other,
            'pupils': pupils,
            'students': students,
            'employees': employees,
        }

    def to_xml(self):
        price_elements = []
        for role, amount in sorted(self.prices.items()):
            if amount is not None:
                price_element = ET.Element('price')
                price_format = "{:0,.2f}"
                price_element.text = price_format.format(amount / 100)
                price_element.set('role', role)

                price_elements.append(price_element)

        return price_elements

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Notes:
    def __init__(self, note_list=None):
        self.note_list = sorted(note_list) if note_list is not None else []

    def to_xml(self):
        note_elements = []
        for note in self.note_list:
            note_element = ET.Element('note')
            note_element.text = note

            note_elements.append(note_element)

        return note_elements

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
