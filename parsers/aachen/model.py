class Category:
    def __init__(self, name, price=None):
        self.name = name
        self.price = price
        self.meals = []

    def append(self, meal):
        self.meals.append(meal)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Meal:
    def __init__(self, name, note_keys=None):
        self.name = name
        self.note_keys = note_keys or set()

    def __repr__(self):
        fields = self.__dict__
        fields['note_keys'] = list(sorted(self.note_keys))
        return '<{}: {}>'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        self_fields = self.__dict__
        self_fields['note_keys'] = list(sorted(self.note_keys))

        other_fields = other.__dict__
        other_fields['note_keys'] = list(sorted(other.note_keys))

        return self_fields == other_fields
