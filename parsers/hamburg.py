from bs4 import BeautifulSoup
import re
import requests
from utils import Parser
from pyopenmensa.feed import LazyBuilder, extractDate, buildPrices


def parse_week(url: str, location_id: str, canteen: LazyBuilder):
    r = requests.get(url)
    if not r.status_code == 200:
        return
    soup = BeautifulSoup(r.text, "lxml")
    # get all menus of this week for the given location_id
    mensa_data_per_location = soup.find(
        "div",
        {"class": "container-fluid px-0 tx-epwerkmenu-menu-location-container", "data-location-id": location_id}
    )
    if mensa_data_per_location is None:
        print('currently no data for this week available')
        return

    canteen.name = soup.find("h5", class_="mensainfo__title").text.strip()
    canteen.address = " ".join(soup.find("a", class_="infocard__link").text.strip().split())

    for category in mensa_data_per_location.find_all(
            "div", class_="tx-epwerkmenu-menu-timestamp-wrapper tx-epwerkmenu-menu-timestamp-active"):
        day = extractDate(category['data-timestamp'])
        category_name = category.find_next("h5", class_="menulist__categorytitle").text.strip()
        meals = category.find_all("div", class_="singlemeal")
        if not meals:
            continue
        for meal in meals:
            # sometimes meals are not grabable - maybe a bug!
            try:
                meal_name = meal.find("h5", class_="singlemeal__headline singlemeal__headline--").text.strip()
            except AttributeError:
                continue
            # get rid of everything in brackets (allergens, and co.)
            meal_name = re.sub("[\(\[].*?[\)\]]", "", meal_name)
            price_dict = {}
            allergens_list = []
            prices = meal.find("div", class_="col-12 col-xl-auto offset-xl-1 col-custom-2 mb-3 mb-xl-0")
            for price in prices.find_all("span", class_="singlemeal__info"):
                price_num = price.text.strip().split("€")[0]
                if "stud" in price.text.strip().lower():
                    price_dict["student"] = price_num
                elif "bedienst" in price.text.strip().lower():
                    price_dict["employee"] = price_num
                elif "gäst" in price.text.strip().lower():
                    price_dict["other"] = price_num
            for allergen in meal.find_all("dd", class_="dlist__item dlist__item--inline"):
                allergens_list.append(allergen.text.strip().split("\n")[0])
            canteen.addMeal(
                date=day,
                category=category_name,
                name=meal_name,
                prices=buildPrices(price_dict),
                notes=allergens_list
            )


def parse_url(url, today=False):
    canteen = LazyBuilder()
    canteen.city = "Hamburg"

    location_id = url[-3:]
    parse_week(url=url, location_id=location_id, canteen=canteen)
    return canteen.toXMLFeed()


parser = Parser('hamburg', handler=parse_url,
                shared_prefix='https://www.studierendenwerk-hamburg.de/speiseplan-nocache?t=this_week&')
parser.define('alexanderstraße', suffix='l=176')
parser.define('armgartstraße', suffix='l=174')
parser.define('bergedorf', suffix='l=168')
parser.define('berliner-tor', suffix='l=170')
parser.define('botanischer-garten', suffix='l=156')
parser.define('bucerius-law-school', suffix='l=162')
parser.define('cafe-cfel', suffix='l=177')
parser.define('cafe-jungiusstrasse', suffix='l=175')
parser.define('cafe-alexanderstrasse', suffix='l=')
parser.define('campus', suffix='l=142')
parser.define('finkenau', suffix='l=174')
parser.define('geomatikum', suffix='l=151')
parser.define('harburg', suffix='l=158')
parser.define('ins-gruene-harburg', suffix='l=159')
parser.define('hcu', suffix='l=166')
parser.define('ueberseering', suffix='l=154')
parser.define('stellingen', suffix='l=161')
parser.define('studierendenhaus', suffix='l=137')
parser.define('mittelweg', suffix='l=178')
parser.define('cafe-zessP', suffix='l=383')
parser.define('cafe-del-arte', suffix='l=148')
parser.define('food-truck', suffix='l=179')
parser.define('schlueters', suffix='l=148')
