#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup
from functools import partial

meal_regex = re.compile(r"""(?P<mealName>.+[^\s])\s*
                            (?P<mealType>\b[A-Z]+)\s*
                            (?P<price>\d+,\d{2})""", re.VERBOSE)
additions_regex = re.compile(r"""(\((\d\s*,?\s*)+\))\s*""", re.VERBOSE)
typeLegend_regex = re.compile(r"""\(([A-Z])\)\s*
                                  ([^#]+)#?""", re.VERBOSE)
additionsLegend_regex = re.compile(r"""\((\d+)\)\s*
                                       ([^#]+)#?""", re.VERBOSE)

def parse_url(url, today=False):

    canteen = LazyBuilder()
    canteen.setAdditionalCharges('student', {}) # TODO: add 'others' - +1€ ? not found on website

    soup = BeautifulSoup(urlopen(url).read())

    mealTypes = {}
    additionsMapping = {}
    for legende in soup.find_all('div', {'class' : 'legende'}):
        for le in typeLegend_regex.findall(legende.string):
            mealTypes[le[0]] = le[1].strip()
        for le in additionsLegend_regex.findall(legende.string):
            additionsMapping[le[0]] = le[1].strip()

    sp_table = soup.find("table", { "class" : "spk_table" } )

    dates = []
    for datecell in sp_table.find_all("td", { "class" : "hl_date" }):
        dates.append(datecell.string)

    subCanteen = None

    dateRow = True
    for row in sp_table.find_all("tr"):

        if(dateRow):
            # we have already handled this
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
                mealType, price = priceTypeMatch.group('mealType', 'price')
                mealType = mealType.strip()

                name = priceTypeMatch.group('mealName')

                # remove (1,2,4) additions specifiers from name & store them in a set()
                additions = set()
                def adder(match, additions):
                    for a in match.group(0).strip('() \t').split(','):
                        additions.add(a)
                    return ''
                name = additions_regex.sub(partial(adder, additions=additions), name).strip()

                notes = []

                for a in additions:
                    notes += [additionsMapping[a.strip()]]

                for mealTypeChar in mealType:
                    notes += [mealTypes[mealTypeChar]]

                canteen.addMeal(date=dates[dateIdx], category=subCanteen, name=name, prices=price, notes=notes)

    return canteen.toXMLFeed()

