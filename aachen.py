#!python3
from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{2}\. ?\d{2}\. ?\d{4})')
day_range_regex = re.compile('(?P<from>\d{2}\.\d{2}).* (?P<to>\d{2}\.\d{2}\.(?P<year>\d{4}))')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
extra_regex = re.compile('\(([0-9,A-N,.,,]+)\)')
legend = {
            "1": "mit Farbstoff",
            "2": "mit Konservierungsstoff",
            "3": "mit Antioxidationsmittel",
            "4": "mit Geschmacksverstärker",
            "5": "geschwefelt",
            "6": "geschwärzt",
            "7": "gewachst",
            "8": "mit Phosphat",
            "9": "mit Süßungsmittel",
            "10": "enthält eine Phenylalaninquelle",
            "A": "enthält glutenhaltiges Getreide",
            "B": "enthält Sellerie",
            "C": "enthält Krebstiere",
            "D": "enthält Eier",
            "E": "enthält Fisch",
            "F": "enthält Erdnüsse",
            "G": "enthält Sojabohnen",
            "H": "enthält Milch (inkl. Lactose)",
            "I": "enthält Schalenfrüchte (Nüsse)",
            "J": "enthält Senf",
            "K": "enthält Sesamsamen",
            "L": "enthält Schwefeldioxid/Sulfite",
            "M": "enthält Lupinen",
            "N": "enthält Weichtiere",
        }

def legendReferences(aMeal):
    foundElements = extra_regex.findall(aMeal)
    foundElements = ','.join(foundElements)
    foundElements = foundElements.replace('.', ',')
    foundElements = foundElements.split(',')

    return sorted(set(foundElements))

def parse_table(table, canteen):
    # iterator about all rows of the table
    rowIter = iter(table.find_all('tr'))
    # extra category names from th's of first row
    headRow = next(rowIter)
    for br in headRow.find_all('br'):
        br.replace_with(' - ')

    categories = list()
    for aHeadRow in headRow.find_all('th')[1:]:
        aCategory = aHeadRow.text.strip().replace('\n', '')

        if aCategory[-2:] == ' -':
            aCategory = aCategory[:-2]

        if aCategory == '-':
            aCategory = 'Spezialmenü'

        if not aCategory in categories:
            categories.append(aCategory)

    try:
        while True:
            # meal row
            tr = next(rowIter)
            
            # get rid of any unneccessary newlines
            if '\n' in tr.contents:
                tr.contents.remove('\n')

            # extract date from first column:
            print("Mäh: " + tr.contents[0].text)
            print("Muh: " + str(day_regex.search(tr.contents[0].text)))
            dateResults = day_regex.search(tr.contents[0].text)
            if dateResults is None:
                continue
            else:
                date = dateResults.group('date')
                if tr.contents[0].get('rowspan') is None:
                    canteen.setDayClosed(date)
                    continue

            # extract information from addition meal component row
            extratr = next(rowIter)
            extratrtext = extratr.text
            if "Kennzeichnung" in extratrtext:
                extratrtext = extratrtext[:extratrtext.index("Kennzeichnung")]
            extratrtext = extratrtext.replace('\xa0', ' ').replace('\n', '').replace('\r', '').replace('\t', '').replace('  ', ' ').strip();
            if extratrtext == '–':
                extras = [];
            else:
                extras = extratrtext.split(' – ')

            # build iterators for lists:
            categoriesIterator = iter(categories)
            colIter = iter(tr.find_all('td'))
            extraIter = iter(extratr.find_all('td'))

            # skip first row (date):
            next(colIter)
            next(extraIter)

            # add meals
            try:
                while True:
                    # get next category
                    category = next(categoriesIterator)

                    # get meal text
                    rawMeals = next(colIter).text;
                    rawMeals = ' '.join(rawMeals.split())

                    # split meal text into multiple meals
                    mainMeals = rawMeals.split(' oder ')

                    # get price
                    price = next(colIter).text
                    if price.strip() == '€':  # no real price available
                        price = None

                    for aMainMeal in mainMeals:
                        # extract notes from name
                        legendRefs = legendReferences(aMainMeal)
                        notes = [legend[v] for v in legendRefs if v in legend]
                        notes.sort()

                        # remove notes from name
                        aMainMeal = extra_regex.sub('', aMainMeal).replace('\xa0', ' ').replace('  ', ' ').strip()

                        # beautify the name
                        aMainMeal = aMainMeal.replace(' , ', ', ').replace(' .', '.').replace('\n', '')
                        if aMainMeal[-2:] == ' -':
                            aMainMeal = aMainMeal[:-2]

                        # add meal
                        if len(aMainMeal) > 0:
                            canteen.addMeal(date, category, aMainMeal, notes, price)
            except StopIteration:
                pass

            if len(extras) >= 1:
                mainExtras = extras[0].replace('Hauptbeilage: ', ' ').split(' oder ')
                # add main extra
                try:
                    for aMainExtra in mainExtras:
                        # extract notes from name
                        legendRefs = legendReferences(aMainExtra)
                        notes = [legend[v] for v in legendRefs if v in legend]
                        notes.sort()

                        # remove notes from name
                        aMainExtra = extra_regex.sub('', aMainExtra).replace('\xa0', ' ').replace('  ', ' ').strip()
                        # beautify the name
                        aMainMeal = aMainMeal.replace(' , ', ', ').replace(' .', '.')
                        if aMainMeal[-2:] == ' -':
                            aMainMeal = aMainMeal[:-2]
                        # add extra
                        if len(aMainMeal) > 0:
                            canteen.addMeal(date, 'Hauptbeilagen', aMainExtra, notes)
                except StopIteration:
                    pass

            if len(extras) >= 2:
                sideExtras = extras[1].replace('Gemüse/Salat: ', ' ').split(' oder ')
                # add side extra
                try:
                    for aSideExtra in sideExtras:
                        # extract notes from name
                        legendRefs = legendReferences(aSideExtra)
                        notes = [legend[v] for v in legendRefs if v in legend]
                        notes.sort()
                        
                        # remove notes from name
                        aSideExtra = extra_regex.sub('', aSideExtra).replace('\xa0', ' ').replace('  ', ' ').strip()
                        # beautify the name
                        aMainMeal = aMainMeal.replace(' , ', ', ').replace(' .', '.')
                        if aMainMeal[-2:] == ' -':
                            aMainMeal = aMainMeal[:-2]
                        # add extra
                        if len(aMainMeal) > 0:
                            canteen.addMeal(date, 'Gemüse/Salat', aSideExtra, notes)
                except StopIteration:
                    pass
    except StopIteration:
        pass

def parse_week(url, data, canteen):
    document = parse(urlopen(url, data).read())

    data = document.find_all('table', 'wo_std')
    if not data:
        message = document.find('div', 'Meldung_std')
        if message:
            m = day_range_regex.search(message.text)
            if m:
                fromDate = datetime.datetime.strptime(m.group('from') + '.' + m.group('year'), '%d.%m.%Y')
                toDate = datetime.datetime.strptime(m.group('to'), '%d.%m.%Y')
                while fromDate <= toDate:
                    canteen.setDayClosed(fromDate.strftime('%Y-%m-%d'))
                    fromDate += datetime.date.resolution
        return
    
    for aTable in data:
        parse_table(aTable, canteen)

def parse_url(url, today=False):
    canteen = OpenMensaCanteen()
    canteen.setAdditionalCharges('student', {'other': 1.5})
    document = parse(urlopen(url).read())
    for submit in document.find_all('input'):
        if submit['type'] != 'submit':
            continue
        parse_week(url, urlencode({submit['name']: submit['value']}).encode('utf8'), canteen)
        if today:
            break
    return canteen.toXMLFeed()

def parse_url_academica(url, today=False):
    canteen = OpenMensaCanteen()
    canteen.setAdditionalCharges('student', {'other': 1.5})
    document = parse(urlopen(url).read())
    parse_week(url, None, canteen)
    return canteen.toXMLFeed()
