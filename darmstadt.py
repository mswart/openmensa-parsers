#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup
from functools import partial

meal_regex = re.compile(r"""(?P<mealName>.+[^\s])\s*
                            (?P<mealType>\b[A-Z]+)\s*
                            (?P<price>\d+,\d{2})""", re.VERBOSE)
additions_regex = re.compile(r"""(\((\d\s*,?\s*)+\))\s*""")

typeLegend_regex = re.compile(r"""\(([A-Z])\)\s*
                                  ([^#]+)#?""", re.VERBOSE)
additionsLegend_regex = re.compile(r"""\((\d+)\)\s*
                                       ([^#]+)#?""", re.VERBOSE)

def parse_week(url, canteen):

    soup = BeautifulSoup(urlopen(url).read())

    mealTypes = {}
    additionsMapping = {}
    for legende in soup.find_all('div', {'class' : 'legende'}):
        for le in typeLegend_regex.findall(legende.string):
            mealTypes[le[0]] = le[1].strip()
        for le in additionsLegend_regex.findall(legende.string):
            additionsMapping[le[0]] = le[1].strip()

    sp_table = soup.find("table", { "class" : "spk_table" } )
    if sp_table is None:
        # call setDayClosed() on current dates ?
        return canteen.toXMLFeed()

    dates = []
    subCanteen = None

    dateRow = True
    for row in sp_table.find_all("tr"):

        if dateRow:
            for datecell in row.find_all("td"):
                if len(datecell.string.strip()) > 0:
                    dates.append(datecell.string)

            if len(dates) == 0:
                # call setDayClosed() on current dates ?
                return canteen.toXMLFeed()

            dateRow = False
            continue
        dateIdx = -2

        subCanteenColumn = True
        for mealCell in row.find_all("td"):
            dateIdx += 1

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
                    print('error in regex matching meal')
                    canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=mealCellText)
                    continue
                name, mealType, price = priceTypeMatch.group('mealName', 'mealType', 'price')

                notes = []

                for mealTypeChar in mealType.strip():
                    notes += [mealTypes[mealTypeChar]]

                # remove "(1,2,4)" additions specifiers from name & store them in a set()
                additions = set()
                def adder(match, additions):
                    for a in match.group(0).strip('() \t').split(','):
                        additions.add(a)
                    return ''
                name = additions_regex.sub(partial(adder, additions=additions), name).strip()

                for a in additions:
                    notes += [additionsMapping[a.strip()]]

                canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=name, prices=price, notes=notes)


#TODO: what does that "today" mean?
def parse_url(url, today, *weeks):
    canteen = LazyBuilder()
    canteen.setAdditionalCharges('student', { })
    for week in weeks:
        parse_week(url + week, canteen)
    
    return canteen.toXMLFeed()

