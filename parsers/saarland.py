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

UTC_DATE_STRING = "%Y-%m-%dT%H:%M:%S.%fZ"

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


def get_notices(notices):
    global base_data

    notices_special = []
    notices_allergens = []
    notices_others = []

    for notice_short in notices:
        notice = base_data['notices'][notice_short]
        if notice['isAllergen']:
            notices_allergens.append(
                'enthält %s (Allergen)' % notice['displayName'])
        else:
            if notice_short == 'nsf':  # ohne Schweinefleisch
                notices_others.append(notice['displayName'])
            elif notice_short in SPECIAL_NOTICES:
                notices_special.append(notice['displayName'])
            else:
                notices_others.append('mit %s' % notice['displayName'])

    return notices_special + notices_allergens + notices_others


def build_notes(notices, components):
    global base_data

    components_all = []

    notices_list = get_notices(notices)

    for component in components:
        component_string = 'dazu ' + component['name']
        if len(component['notices']) > 0:
            component_notices_list = get_notices(component['notices'])
            component_string += ' (%s)' % ', '.join(component_notices_list)
        components_all.append(component_string)

    return components_all + notices_list


def build_hours(opening_hours):
    if not opening_hours:
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

    canteen = LazyBuilder()
    with urlopen(url) as response:
        data = json.loads(response.read().decode())

    for day in data['days']:
        date = day.get('date')

        if today and (datetime.datetime.now().date() !=
                      datetime.datetime.strptime(date, UTC_DATE_STRING).date()):
            continue

        for counter in day['counters']:
            counter_name = counter['displayName']
            counter_description = counter['description']
            counter_hours = counter.get('openingHours')
            counter_color = counter.get('color')

            for meal in counter['meals']:
                if 'knownMealId' in meal:
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


with urlopen(URL_BASE + URL_BASE_DATA) as response:
    data = json.loads(response.read().decode())
base_data = {}
base_data['locations'] = []
base_data['roles'] = {}

base_data['notices'] = data['notices']
for loc in data['locations']:
    base_data['locations'].append(loc)
for role in data['priceTiers']:
    if role not in ROLES:
        print('New unknown price tier: %s (displayName: %s)' %
              (role, data['priceTiers'][role]))
        print('All prices for this price tier will be ignored.')
        print('Please consider updating the parser!')
    else:
        base_data['roles'][role] = ROLES[role]


parser = Parser('saarland',
                handler=parse_url,
                shared_prefix=URL_BASE + URL_MENU)

for loc in base_data['locations']:
    parser.define(loc, suffix=loc)
