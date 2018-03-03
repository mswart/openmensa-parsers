from model.openmensa_model import Notes, Prices


class PricesBuilder:
    def __init__(self, other=None, pupils=None, students=None, employees=None):
        """

        :param int other:
        :param int pupils:
        :param int students:
        :param int employees:
        """
        if all(role is None for role in [other, pupils, students, employees]):
            raise ValueError("DefaultPriceBuilder awaits an amount for at least one of the roles "
                             "others, pupils, students or employees.")
        self.supplements = {
            'other': other,
            'pupils': pupils,
            'students': students,
            'employees': employees
        }

    def build_prices(self, default):
        """

        :param int default:
        :rtype: Prices
        """
        actual_price_kwargs = {
            role: default + supplement for role, supplement in self.supplements.items()
            if supplement is not None
        }
        return Prices(**actual_price_kwargs)


class NotesBuilder:
    def __init__(self, legend, ignore_not_found=False):
        """

        :param dict[string, string] legend:
        """
        self.legend = legend
        self.ignore_not_found = ignore_not_found

    def build_notes(self, note_keys):
        """

        :param list[string] note_keys:
        :rtype: Notes
        """
        if self.ignore_not_found:
            note_list = [self.legend[key] for key in note_keys if key in self.legend]
        else:
            note_list = [self.legend[key] if key in self.legend else key for key in note_keys]
        return Notes(note_list)
