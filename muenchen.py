#!python3
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import LazyBuilder

price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')
otherPrice = re.compile('Gästezuschlag:? ?(?P<price>\d+[,.]\d{2}) ?€?')

base = 'http://www.studentenwerk-muenchen.de/mensa'


def parse_url(url, today=False):
    canteen = LazyBuilder()
    legend = {'f': 'fleischloses Gericht', 'v': 'veganes Gericht'}
    document = parse(urlopen(base + '/speiseplan/zusatzstoffe-de.html').read())
    for td in document.find_all('td', 'beschreibung'):
        legend[td.previous_sibling.previous_sibling.text] = td.text
    document = parse(urlopen(base + '/unsere-preise/').read())
    prices = {}
    for tr in document.find('table', 'essenspreise').find_all('tr'):
        meal = tr.find('th')
        if not meal or not meal.text.strip():
            continue
        if len(tr.find_all('td', 'betrag')) < 3:
            continue
        if 'class' in meal.attrs and 'titel' in meal.attrs['class']:
            continue
        meal = meal.text.strip()
        prices[meal] = {}
        for role, _id in [('student', 0), ('employee', 1), ('other', 2)]:
            prcie_html = tr.find_all('td', 'betrag')[_id].text
            prices[meal][role] = price_regex.search(prcie_html).group('price')
    errorCount = 0
    date = datetime.date.today()
    while errorCount < 7:
        try:
            document = parse(urlopen(url.format(date)).read())
        except HTTPError as e:
            if e.code == 404:
                errorCount += 1
                date += datetime.date.resolution
                continue
            else:
                raise e
        else:
            errorCount = 0
        for tr in document.find('table', 'zusatzstoffe').find_all('tr'):
            identifier = tr.find_all('td')[0].text \
                           .replace('(', '').replace(')', '')
            legend[identifier] = tr.find_all('td')[1].text.strip()
        canteen.setLegendData(legend)
        mensa_data = document.find('table', 'menu')
        category = None
        for menu_tr in mensa_data.find_all('tr'):
            if menu_tr.find('td', 'headline'):
                continue
            if menu_tr.find('td', 'gericht').text:
                category = menu_tr.find('td', 'gericht').text
            data = menu_tr.find('td', 'beschreibung')
            name = data.find('span').text.strip()
            notes = [span['title'] for span in data.find_all('span', title=True)]
            canteen.addMeal(
                date, category, name, notes,
                prices.get(category.replace('Aktionsessen', 'Bio-/Aktionsgericht'), {})
            )
        date += datetime.date.resolution
        if today:
            break
    return canteen.toXMLFeed()
