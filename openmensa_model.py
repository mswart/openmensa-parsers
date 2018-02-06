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
    def __init__(self, name, price=None, notes=None):
        self.name = name
        self.price = price
        self.notes = notes

    def to_xml(self):
        meal_element = ET.Element('meal')
        name = ET.SubElement(meal_element, 'name')
        name.text = self.name

        for note in sorted(self.notes):
            note_element = ET.SubElement(meal_element, 'note')
            note_element.text = note

        if self.price:
            price_format = "{:0,.2f}"
            if isinstance(self.price, PriceWithRoles):
                for role in sorted(self.price.roles):
                    price = ET.SubElement(meal_element, 'price', {'role': role.name})
                    role_price = self.price.default + role.priceSupplement
                    price.text = price_format.format(role_price / 100)
            else:
                price = ET.SubElement(meal_element, 'price')
                price.text = price_format.format(self.price / 100)

        return meal_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class PriceWithRoles:
    def __init__(self, default, roles):
        self.default = default
        self.roles = roles

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Role:
    def __init__(self, name, price_supplement=0):
        self.name = name
        self.priceSupplement = price_supplement

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __lt__(self, other):
        return isinstance(other, self.__class__) and self.name < other.name
