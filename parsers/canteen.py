class Entry:
    def __init__(self, category_name, meal, price_string=None):
        self.category_name = category_name
        self.meal = meal
        self.price_string = price_string


class Meal:
    def __init__(self, name):
        self.name = name
        self.note_keys = []

    def set_note_keys(self, note_keys):
        self.note_keys = note_keys

    def get_fulltext_notes(self, legend):
        return [legend.get(n, n) for n in sorted(self.note_keys) if n]
