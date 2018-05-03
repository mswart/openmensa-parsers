from urllib.request import *

import json
import datetime

from pyopenmensa.feed import LazyBuilder

from utils import Parser, Source


API_VERSION = "1"
# please don't copy this key, contact felix@fefrei.de to get your own instead
API_KEY = "A1RT5M56" + "ibsGaGNZBJQg"
APP_VERSION = "1"
SUPPORTED_LANGUAGES = ["de", "en"]

URL_BASE = (
    'https://mensaar.de/api/%s/%s/%s/%s/'
    % (API_VERSION, API_KEY, APP_VERSION, SUPPORTED_LANGUAGES[0])
)
URL_BASE_DATA = "getBaseData"
URL_MENU = "getMenu/"

# mensaar.de always returns an UTC date
UTC_DATE_STRING = "%Y-%m-%dT%H:%M:%S.%fZ"

LOCATIONS = [
    'sb',
    'hom',
    'musiksb',
    'htwgtb',
    'mensagarten'
]

ROLES = {
    's': 'student',
    'g': 'other',
    'm': 'employee'
}

SPECIAL_NOTICES = [
    'su',   # geschwefelt
    'bl',   # geschwärzt
    'gw',   # gewachst
    've',   # vegetarisch
    'bio',  # biologisches Essen
    'nla',  # laktosefrei
    'vn'    # vegan
]

NOTICES_PREFIX_COMPLEMENT = "dazu"
NOTICES_PREFIX_ALLERGENS = "enthält"
NOTICES_PREFIX_OTHERS = "mit"


def get_notices(notices, sub_notices=False):
    global base_data

    notices_special = []
    notices_allergens = []
    notices_others = []
    notices_others_last = []

    for notice_short in notices:
        notice = base_data['notices'][notice_short]
        if notice['isAllergen']:
            if sub_notices:
                notices_allergens.append(notice['displayName'])
            else:
                notices_allergens.append(
                    '%s %s' % (NOTICES_PREFIX_ALLERGENS, notice['displayName']))
        else:
            if notice['isNegated']:
                notices_others_last.append(notice['displayName'])
            elif notice_short in SPECIAL_NOTICES:
                notices_special.append(notice['displayName'])
            else:
                if sub_notices:
                    notices_others.append(notice['displayName'])
                else:
                    notices_others.append(
                        '%s %s' % (NOTICES_PREFIX_OTHERS, notice['displayName']))

    if sub_notices:
        notices_allergens = build_subnotices(notices_allergens, NOTICES_PREFIX_ALLERGENS)
        notices_others = build_subnotices(notices_others, NOTICES_PREFIX_OTHERS)

    return (notices_special + notices_allergens +
            notices_others + notices_others_last)


def build_subnotices(notices, prefix):
    if len(notices) > 0:
        notices[0] = '%s %s' % (prefix, notices[0])
    if len(notices) > 1:
        notices[-2] = (
            '%s und %s' % (notices[-2], notices[-1]))
        del notices[-1]
    return notices


def build_notes(notices, components):
    components_all = []

    notices_list = get_notices(notices)

    for component in components:
        component_string = '%s %s' % (NOTICES_PREFIX_COMPLEMENT, component['name'])
        if len(component['notices']) > 0:
            component_notices_list = get_notices(component['notices'], True)
            component_string += ' (%s)' % ', '.join(component_notices_list)
        components_all.append(component_string)

    return components_all + notices_list


def build_hours(opening_hours):
    if opening_hours is None:
        return []

    start = datetime.datetime.strptime(
        opening_hours['start'], UTC_DATE_STRING).time()
    end = datetime.datetime.strptime(
        opening_hours['end'], UTC_DATE_STRING).time()
    return [
        'verfügbar von %s bis %s Uhr' %
        (datetime.time.strftime(start, "%H:%M"),
            datetime.time.strftime(end, "%H:%M"))
    ]


def build_location(description):
    return ['Ort: %s' % description] if description else []


def parse_url(url, today=False):
    global base_data

    load_base_data()

    canteen = LazyBuilder()
    with urlopen(url) as response:
        data = json.loads(response.read().decode())

    for day in data['days']:
        date = datetime.datetime.strptime(day['date'], UTC_DATE_STRING).date()

        if today and (datetime.date.today() != date):
            continue

        for counter in day['counters']:
            counter_name = counter['displayName']
            counter_description = counter['description']
            counter_hours = counter.get('openingHours')

            for meal in counter['meals']:
                if 'knownMealId' in meal:
                    # This is meant to allow recognizing recurring meals,
                    # for features like marking meals as favorites.
                    # Up to now, not really used in the mensaar.de API.
                    print('knownMealId: %s' % meal['knownMealId'])

                meal_name = meal['name']
                if 'category' in meal:
                    meal_name = '%s: %s' % (meal['category'], meal_name)

                meal_notes = (
                    build_location(counter_description) +
                    build_hours(counter_hours) +
                    build_notes(meal['notices'], meal['components']))

                meal_prices = {}
                if 'prices' in meal:
                    prices = meal['prices']
                    for role in prices:
                        if role in base_data['roles']:
                            meal_prices[base_data['roles'][role]] = prices[role]
                        else:
                            print('Ignoring price for unknown role %s.' % role)

                if 'pricingNotice' in meal:
                    meal_notes.append(meal['pricingNotice'])

                canteen.addMeal(date, counter_name,
                                meal_name, meal_notes, meal_prices)

    return canteen.toXMLFeed()


def load_base_data():
    with urlopen(URL_BASE + URL_BASE_DATA) as response:
        data = json.loads(response.read().decode())

    base_data['roles'] = {}

    base_data['notices'] = data['notices']
    for loc in data['locations']:
        if loc not in LOCATIONS:
            # Found an unknown location
            # Please consider updating the parser!
            raise RuntimeError(
                'Unknown location: %s (displayName: %s)' %
                (loc, data['locations'][loc]))
    for role in data['priceTiers']:
        if role not in ROLES:
            # Found an unknown price tier
            # All prices for this price tier will be ignored.
            # Please consider updating the parser!
            raise RuntimeError(
                'Unknown price tier: %s (displayName: %s)' %
                (role, data['priceTiers'][role]))
        else:
            base_data['roles'][role] = ROLES[role]


base_data = {}

parser = Parser('saarland',
                handler=parse_url,
                shared_prefix=URL_BASE + URL_MENU)

for loc in LOCATIONS:
    parser.define(loc, suffix=loc)
