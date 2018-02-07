import lxml.etree as ET


class Canteen:
    def __init__(self):
        self.days = []

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


class DayClosed:
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
    def __init__(self, name):
        self.name = name
        self.meals = []

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
        self.notes = notes

    def to_xml(self):
        meal_element = ET.Element('meal')
        name = ET.SubElement(meal_element, 'name')
        name.text = self.name

        for note in sorted(self.notes):
            note_element = ET.SubElement(meal_element, 'note')
            note_element.text = note

        for price in sorted(self.prices):
            price_element = price.to_xml()
            meal_element.append(price_element)

        return meal_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Price:
    def __init__(self, amount, role=None):
        self.amount = amount
        self.role = role

    def to_xml(self):
        price_element = ET.Element('price')
        price_format = "{:0,.2f}"
        price_element.text = price_format.format(self.amount / 100)

        if self.role:
            price_element.set('role', self.role)

        return price_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Cannot compare type '{}' with type '{}'.".format(type(self), type(other)))
        return self.role < other.role
