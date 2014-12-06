#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup
from functools import partial

meal_regex = re.compile(r"""(?P<mealName>.+\S)\s*
                            (?P<mealType>\b[A-Z]+)\s*
                            (?P<price>\d+,\d{2})?""", re.VERBOSE)

typeLegend_regex = re.compile(r"""\(([A-Z])\)\s*
                                  ([^#]+)#?""", re.VERBOSE)

def parse_week(url, canteen):

    soup = BeautifulSoup(urlopen(url).read())

    mealTypes = {}
    try:
        for legendTag in soup.find_all('div', {'class' : 'legende'}):
            for le in typeLegend_regex.findall(legendTag.string):
                mealTypes[le[0]] = le[1].strip()
            canteen.setLegendData(text=legendTag.string, legend=canteen.legendData)
    except:
        pass

    sp_table = soup.find("table", { "class" : "spk_table" } )
    if sp_table is None:
        #TODO: call setDayClosed() on current dates ?
        return

    dates = []
    subCanteen = None

    dateRow = True
    for row in sp_table.find_all("tr"):

        if dateRow:
            for datecell in row.find_all(["td", "th"]):
                if len(datecell.string.strip()) > 0:
                    dates.append(datecell.string)

            if len(dates) == 0:
                #TODO: call setDayClosed() on current dates ?
                return

            dateRow = False
            continue
        dateIdx = -2

        subCanteenColumn = True
        for mealCell in row.find_all("td"):
            dateIdx += 1

            if dateIdx >= len(dates):
                print('broken page: content cells without header')
                break

            #TODO: setDayClosed()

            mealCellText = mealCell.find(text=True)
            mealCellText = mealCellText.strip()

            if subCanteenColumn and len(mealCellText) > 0:
                subCanteen = mealCellText
                if subCanteen == "Marktrest.":
                    subCanteen = "Marktrestaurant"
                subCanteenColumn = False
                continue
            subCanteenColumn = False

            if len(mealCellText) > 0:

                priceTypeMatch = meal_regex.match(mealCellText)
                if priceTypeMatch is None:
                    print('regex not matching meal: "{}"'.format(mealCellText))
                    canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=mealCellText)
                    continue
                name, mealType, price = priceTypeMatch.group('mealName', 'mealType', 'price')

                notes = []

                if mealType:
                    for mealTypeChar in mealType.strip():
                        if mealTypeChar in mealTypes:
                            notes += [mealTypes[mealTypeChar]]

                canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=name, prices=price, notes=notes)


def parse_url(url, today):
    canteen = LazyBuilder()
    canteen.setAdditionalCharges('student', { })
    if today:
        parse_week(url, canteen) # base url only contains current day
    else:
        parse_week(url + 'week', canteen)
        parse_week(url + 'nextweek', canteen)
    
    return canteen.toXMLFeed()

