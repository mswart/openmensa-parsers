import os

import lxml.etree as ET

base_directory = os.path.dirname(os.path.realpath(__file__))


class Canteen:
    def __init__(self, days=None):
        """

        :param list[Day | ClosedDay] days:
        """
        self.days = days or []

    def to_string(self, pretty_print=True):
        """

        :param bool pretty_print:
        :rtype: str
        """

        feed_string = ET.tostring(
            self.to_xml(),
            encoding='UTF-8',
            pretty_print=pretty_print
        ).decode('utf-8')
        feed_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + feed_string

        schema = ET.XMLSchema(file=os.path.join(base_directory, "open-mensa-v2.xsd"))
        parser = ET.XMLParser(schema=schema)
        ET.fromstring(feed_string.encode("utf-8"), parser)  # will raise error if invalid

        return feed_string

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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
    def __init__(self, date, categories):
        """

        :param datetime.date date:
        :param list[Category] categories:
        """
        self.date = date
        if len(categories) == 0:
            raise ValueError("Categories cannot be empty. You can use a `ClosedDay` instead.")
        self.categories = categories

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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
        """

        :param datetime.date date:
        """
        self.date = date

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
        day_element = ET.Element('day', {'date': self.date.isoformat()})
        ET.SubElement(day_element, 'closed')
        return day_element

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Category:
    def __init__(self, name, meals=None):
        """

        :param str name:
        :param list[Meal] meals:
        """
        self.name = name
        self.meals = meals or []

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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
        """

        :param str name:
        :param Prices prices:
        :param Notes notes:
        """
        self.name = name
        self.prices = prices
        self.notes = notes or Notes()

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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


class Prices:
    def __init__(self, other=None, pupil=None, student=None, employee=None):
        """

        :param int other:
        :param int pupil:
        :param int student:
        :param int employee:
        """
        if all(role is None for role in [other, pupil, student, employee]):
            raise ValueError("Prices awaits an amount for at least one of the roles "
                             "others, pupils, students or employees.")

        self.prices = {
            'other': other,
            'pupil': pupil,
            'student': student,
            'employee': employee,
        }

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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
        """

        :param list[str] note_list:
        """
        self.note_list = sorted(note_list) if note_list is not None else []
        if any(len(note) == 0 for note in self.note_list):
            raise ValueError("Entries in `note_list` cannot be empty.")

    def to_xml(self):
        """

        :rtype: lxml.etree.Element
        """
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
