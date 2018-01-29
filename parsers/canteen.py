from pyopenmensa.feed import convertPrice


class Day:
    def __init__(self, date):
        self.date = date
        self.categories = {}

    def parse_entry(self, entry):
        if entry.category.name not in self.categories:
            self.categories[entry.category.name] = entry.category
        self.categories[entry.category.name].add_meal(entry.meal)


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
        self.meals.append(meal)


class Meal:
    def __init__(self, name, price=None):
        self.name = name
        self.note_keys = []
        self.price = price

    def set_note_keys(self, note_keys):
        self.note_keys = note_keys

    def set_price_from_string(self, price_string):
        self.price = convertPrice(price_string)
