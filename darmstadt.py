#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup

from utils import Parser

price_regex = re.compile(r"""(\d+,\d{2}\s*€)""")
legend_tag_regex = r'(?P<name>(\d|[a-zA-Z])+)\)\s*' + \
                   r'(?P<value>\w+((\s+\w+)*[^0-9)]))'


def parse_week(url, canteen):
    soup = BeautifulSoup(urlopen(url).read())

    try:
        for legendTag in soup.find_all('div', {'class': 'legende'}):
            canteen.setLegendData(text=legendTag.string,
                    legend=canteen.legendData,
                    regex=legend_tag_regex)
    except Exception as e:
        print('Error in parsing legend ' + e)

    sp_table = soup.find("table", {"class": "spk_table"})
    if sp_table is None:
        print("No meal data on this page")
        return

    dates = []
    subCanteen = None

    is_date_row = True
    for row in sp_table.find_all("tr"):

        if is_date_row:
            for datecell in row.find_all(["td", "th"]):
                if len(datecell.string.strip()):
                    dates.append(datecell.string)

            if len(dates) == 0:
                print("No dates for meal data on this page")
                return

            is_date_row = False
            continue
        dateIdx = -2

        subCanteenColumn = True
        for mealCell in row.find_all("td"):
            dateIdx += 1

            if dateIdx >= len(dates):
                print('broken page: content cells without header')
                break

            mealCellText = mealCell.find(text=True).strip()

            # heading column for subCanteen/"Essensausgabe"
            if subCanteenColumn and len(mealCellText):
                subCanteen = mealCellText
                if subCanteen == "Marktrest.":
                    subCanteen = "Marktrestaurant"
                subCanteenColumn = False
                continue
            subCanteenColumn = False

            if not len(mealCellText):
                continue

            if "geschlossen" in mealCellText:
                setDayClosed(dates[dateIdx])

            # extract price tag
            _prices = price_regex.split(mealCellText)
            if len(_prices) == 3:
                name, price, n2 = _prices
                name = name + n2
            else:
                # multiple prices for a meal - keep all of them literally
                name = mealCellText
                price = None

            canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=name, prices=price)


def parse_url(url, today):
    canteen = LazyBuilder()
    canteen.setAdditionalCharges('student', {})
    if today:
        parse_week(url, canteen)  # base url only contains current day
    else:
        parse_week(url + 'week', canteen)
        parse_week(url + 'nextweek', canteen)

    return canteen.toXMLFeed()


parser = Parser('darmstadt', handler=parse_url,
                shared_prefix='https://www.stwda.de/components/com_spk/')
parser.define('stadtmitte', suffix='spk_Stadtmitte_print.php?ansicht=')
parser.define('lichtwiese', suffix='spk_Lichtwiese_print.php?ansicht=')
parser.define('schoefferstrasse', suffix='spk_Schoefferstrasse_print.php?ansicht=')
parser.define('dieburg', suffix='spk_Dieburg_print.php?ansicht=')
parser.define('haardtring', suffix='spk_Haardtring_print.php?ansicht=')
