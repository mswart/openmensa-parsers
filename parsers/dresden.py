from urllib.request import urlopen
import json
from utils import Parser
from datetime import datetime, timedelta
from pyopenmensa.feed import LazyBuilder

# Grab all dresden canteen information from its public original legit API
API_VERSION = '2'
URL_BASE = 'https://api.studentenwerk-dresden.de/openmensa/v' + API_VERSION + '/'

# Which canteens do we want?
LOCATION = {
    'dresden-reichenbachstrasse': 'Mensa Reichenbachstraße',
    'dresden-zeltschloesschen': 'Zeltschlösschen',
    'dresden-alte-mensa': 'Alte Mensa',
    'dresden-mensologie': 'Mensologie',
    'dresden-siedepunkt': 'Mensa Siedepunkt',
    'dresden-johannstadt': 'Mensa Johannstadt',
    'tharandt-tellerrandt': 'Mensa TellerRandt',
    'dresden-palucca-hochschule': 'Mensa Palucca Hochschule',
    'dresden-wueins': 'Mensa WUeins',
    'dresden-bruehl': 'Mensa Brühl',
    'dresden-stimm-gabel': 'Mensa Stimm-Gabel',
    'dresden-u-boot': 'BioMensa U-Boot',
    'dresden-mensa-sport': 'Mensa Sport',
    'dresden-cafe-cube': 'Grill Cube',
    'dresden-cafe-mobil': 'Pasta-Mobil',
    'zittau-kraatschn': 'Mensa Kraatschn',
    'zittau-mahlwerk': 'Mensa Mahlwerk',
    'goerlitz-mio': 'MiO - Mensa im Osten',
    'rothenburg-mensa': 'Mensa Rothenburg',
    'bautzen-polizeihochschule': 'Mensa Bautzen Polizeihochschule',
    'bautzen-oberschmausitz': 'Mensa Oberschmausitz'
}

# Create a dict where we save the original ids
LOCATION_ID = {}

# Which canteens does studentenwerk dresden have?
with urlopen(URL_BASE + 'canteens') as response:
    canteens = json.loads(response.read().decode())

# Copy the original ids into our dict
for item in canteens:
    for key in LOCATION:
        if LOCATION[key] == item["name"]:
            LOCATION_ID.update({key: item["id"]})


# Returns a list of days that the canteen supports (Format YYYY-MM-DD)
# based on https://doc.openmensa.org/api/v2/canteens/days/ >> "List days of a canteen"
def get_accepted_days(url):
    with urlopen(url + '/days') as response:
        result = json.loads(response.read().decode())
    return result

def validate_prices(prices=None):
    # @Studentenwerk Dresden: it would be nice to remove the two following lines. :-)
    # If it's possible: update your roles
    if prices is None:
        prices = {}
    for key in prices:
        if prices[key] is None:
            prices[key] = float(0)
        else:
            prices[key] = float(prices[key])
    newprices = prices.copy()
    for key in prices:
        if key not in ['student', 'employee', 'pupil', 'other', 'Studierende', 'Bedienstete', 'Schüler']:
            newprices['other'] = prices[key]
            del newprices[key]
    prices = newprices.copy()
    if 'Studierende' in prices:
        prices['student'] = prices['Studierende']
        del prices['Studierende']
    if 'Bedienstete' in prices:
        prices['employee'] = prices['Bedienstete']
        del prices['Bedienstete']
    if 'Schüler' in prices:
        prices['pupil'] = prices['Schüler']
        del prices['Schüler']
    return prices


def parse_today(url, canteen):
    days = get_accepted_days(url)
    # check if today is within the accepted days
    today_time_string = datetime.today().strftime("%Y-%m-%d")
    for day in days:
        if day["date"] == today_time_string:
            if day["closed"]:
                canteen.setDayClosed(today_time_string)
            else:
                with urlopen(url + '/days/' + today_time_string + '/meals') as response:
                    meals = json.loads(response.read().decode())
                    for meal in meals:
                        canteen_prices = validate_prices(meal["prices"])
                        canteen.addMeal(today_time_string, meal["category"], meal["name"], meal["notes"],
                                        canteen_prices)


def parse_full(url, canteen):
    all_days = get_accepted_days(url)
    result_days = {}
    # get first day of timespan - e.g. the first day of this week
    day_begin = (datetime.today() - timedelta(days=datetime.today().weekday())).date()
    # add 14 days, as we need this week + next week
    for i in range(0, 14):
        for day in all_days:
            day_iteration = (day_begin + timedelta(i)).isoformat()  # (str) "2021-08-20"
            if day["date"] == day_iteration:
                # save all 14 days, that we want and their closed-state
                result_days[day["date"]] = day["closed"]
    # for each day set a meal or set closed
    for day in result_days:
        if result_days[day] is True:
            canteen.setDayClosed(day)
        else:
            with urlopen(url + '/days/' + day + '/meals') as response:
                meals = json.loads(response.read().decode())
                for meal in meals:
                    canteen_prices = validate_prices(meal["prices"])
                    canteen.addMeal(day, meal["category"], meal["name"], meal["notes"], canteen_prices)


def parse_url(url, today=False):
    canteen = LazyBuilder()
    if today:
        parse_today(url, canteen)
    else:
        parse_full(url, canteen)
    return canteen.toXMLFeed()


parser = Parser('dresden', handler=parse_url, shared_prefix=URL_BASE + 'canteens/')

# each canteen needs to be defined
for key in LOCATION_ID:
    parser.define(key, suffix=str(LOCATION_ID[key]))
