#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse

from pyopenmensa.feed import LazyBuilder, extractDate


def parse_week(url, canteen, type):
    document = parse(urlopen(url).read())
    for day_table in document.find_all('table', 'swbs_speiseplan'):
        caption = day_table.find('th', 'swbs_speiseplan_head').text
        if type not in caption:
            continue
        date = extractDate(caption)
        for meal_tr in day_table.find_all('tr'):
            if not meal_tr.find('td'):  # z.B Headline
                continue
            tds = meal_tr.find_all('td')
            category = tds[0].text
            name = tds[1].text
            if tds[1].find('a', href='http://www.stw-on.de/mensavital'):
                notes = ['MensaVital']
            else:
                notes = []
            prices = {
                'student':  tds[2].text,
                'employee': tds[3].text,
                'other':    tds[4].text
            }
            canteen.addMeal(date, category, name, notes, prices)


def parse_url(url, type='Mittagsmensa'):
    canteen = LazyBuilder()
    legend_doc = parse(urlopen(url[:url.find('menus/')]
                               + 'wissenswertes/lebensmittelkennzeichnung'))
    canteen.setLegendData(
        text=legend_doc.find(id='artikel').text,
        regex=r'(?P<name>(\d+|[A-Z]+))\s+=\s+(?P<value>\w+( |\t|\w)*)'
    )
    parse_week(url, canteen, type)
    parse_week(url + '-kommende-woche', canteen, type)
    return canteen.toXMLFeed()
