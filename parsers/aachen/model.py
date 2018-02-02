class Category:
    def __init__(self, name, price=None):
        self.name = name
        self.price = price
        self.meals = []

    def add_meal(self, meal):
        self.meals.append(meal)


class Meal:
    def __init__(self, name, note_keys=None):
        self.name = name
        self.note_keys = note_keys or []
