from bs4 import BeautifulSoup
from urllib.request import urlopen
from pyopenmensa.feed import LazyBuilder, buildLegend
from utils import Parser

def parsePlan(url, internalMensaId, today):
    canteen = LazyBuilder()
    end = False
    while (url != None):
        dom = BeautifulSoup(urlopen(url).read(), 'lxml')
        date = dom.select('#mensa_date > p')[0].contents[0]
        menuDefinition = dom.find(id=internalMensaId)
        menuDescription = menuDefinition.parent.find('dd')
        tables = menuDescription.select('table')
        legend = {}
        legend = buildLegend(legend, str(dom), regex='<strong>(?P<name>\w+)\s*</strong>\s*-\s*(?P<value>[\w\s)(]+)')
        if tables != None and len(tables) == 1:
            table = tables[0]
            rows = table.find_all('tr')
            for row in rows:
                menuNameElement = row.select('td[class="mensa_col_55"] > b')
                if menuNameElement != None and menuNameElement[0].contents != None:
                    menuName = menuNameElement[0].contents[0]
                    category = 'Gericht'

                    # get notes
                    notes = {}
                    notesElement = row.select('td[class="mensa_col_55"] > span')
                    if notesElement != None and len(notesElement) > 0 and notesElement[0].text != None:
                        notes = [legend.get(n, n) for n in notesElement[0].text.split(' ') if n]

                    # get prices
                    prices = {}
                    for td in row.select('td[class="mensa_col_15"]'):
                        priceElement = td.find('b')
                        groupElement = td.find('span')
                        if priceElement != None and groupElement != None and groupElement.contents != None and len(groupElement.contents) > 0 and priceElement.contents != None and len(priceElement.contents) > 0:
                            group = str(groupElement.contents[0])
                            price = str(priceElement.contents[0])
                            if group == 'Stud.:':
                                prices['student'] = price
                            elif group == 'Bed.:':
                                prices['employee'] = price
                            elif group == 'Gast:':
                                prices['other'] = price

                    canteen.addMeal(date, category, menuName, notes, prices)
        else:
            canteen.setDayClosed(date)

        # check for further pages
        nextPageLink = dom.find(id='next_day_link')
        if nextPageLink == None or today:
            url = None
        else:
            url = 'https://www.studentenwerk-rostock.de/' + nextPageLink['href']
    return canteen.toXMLFeed()

def parse_url(url, today=False):
    splitted = url.split('#')
    return parsePlan(splitted[0], splitted[1], today)


parser = Parser('rostock', handler=parse_url, shared_prefix='https://www.studentenwerk-rostock.de/de/mensen/speiseplaene.html')
parser.define('mensa-sued', suffix='#mensa_id_1')
parser.define('campus-cafeteria-einstein', suffix='#mensa_id_13')
parser.define('mensa-st-georg-straße', suffix='#mensa_id_2')
parser.define('mensa-multiple-choice', suffix='#mensa_id_14')
parser.define('mensa-kleine-ulme', suffix='#mensa_id_3')
parser.define('mensa-ulme-69', suffix='#mensa_id_8')
parser.define('campus-mensa-wismar', suffix='#mensa_id_5')
