#!/usr/bin/env python3

from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder
import re
from bs4 import BeautifulSoup

meal_regex = re.compile(r"""(?P<mealName>.+)\s*
                            (?P<mealType>\b[SRKLGFV]+)\s*
                            (?P<price>\d+,\d{2})""", re.VERBOSE)
additions_regex = re.compile(r"""(\((\d\s*,?\s*)*\))\s*""", re.VERBOSE)

url = 'http://www.stwda.de/components/com_spk/spk_Stadtmitte_print.php?ansicht=week'

canteen = LazyBuilder()
canteen.setAdditionalCharges('student', {} )

soup = BeautifulSoup(urlopen(url).read())

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
    idx = -2
    subCanteenColumn = True
    for mealCell in row.find_all("td"):
        idx += 1

        mealCellText = mealCell.find(text=True)
        mealCellText = mealCellText.strip()

        if subCanteenColumn and len(mealCellText) > 0:
            subCanteen = mealCellText
            subCanteenColumn = False
            continue
        subCanteenColumn = False

        if len(mealCellText) > 0:
            priceTypeMatch = meal_regex.match(mealCellText)
            if priceTypeMatch is None:
                print('error in regex matching meal')
                canteen.addMeal(date=dates[idx], category=subCanteen, name=mealCellText)
                continue
            mealType, price = priceTypeMatch.group('mealType', 'price')
            mealType = mealType.strip()

            name = priceTypeMatch.group('mealName').rstrip()
            nameAdditionsMatch = additions_regex.search(name) #TODO: repeat, if multiple (1) additions specifiers (1,2,5)
            additions = None
            if not nameAdditionsMatch is None:
                name = (name[:nameAdditionsMatch.start(0)] + name[nameAdditionsMatch.end(0):]).strip()
                additions = nameAdditionsMatch.group(0)

            #TODO: lookup additions specifiers & add as notes=[]
            #TODO: do something with mealType
            #TODO: lookup / prettify subCanteen (Marktrest. -> Marktrestaurant)
            canteen.addMeal(date=dates[idx], category=subCanteen, name=name, prices=price)

print(canteen.toXMLFeed())

