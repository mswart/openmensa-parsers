from pyopenmensa.feed import convertPrice


class Entry:
    def __init__(self, category, meal):
        self.category = category
        self.meal = meal


class Category:
    def __init__(self, name, price=None):
        self.name = name
        self.price = price

    def set_price_from_string(self, price_string):
        self.price = convertPrice(price_string)


class Meal:
    def __init__(self, name):
        self.name = name
        self.note_keys = []

    def set_note_keys(self, note_keys):
        self.note_keys = note_keys

    def get_fulltext_notes(self, legend):
        return [legend.get(n, n) for n in sorted(self.note_keys) if n]
