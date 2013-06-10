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


def parse_url(url, canteentype='Mittagsmensa', legend_url=None, next_week=True):
    canteen = LazyBuilder()
    if not legend_url:
        legend_url = url[:url.find('essen/') + 6] + 'lebensmittelkennzeichnung'
    legend_doc = parse(urlopen(legend_url))
    canteen.setLegendData(
        text=legend_doc.find(id='artikel').text,
        regex=r'(?P<name>(\d+|[A-Z]+))\s+=\s+(?P<value>\w+( |\t|\w)*)'
    )
    parse_week(url, canteen, canteentype)
    if next_week is True:
        parse_week(url + '-kommende-woche', canteen, canteentype)
    if type(next_week) is str:
        parse_week(url + next_week, canteen, canteentype)
    return canteen.toXMLFeed()


def register_canteens(providers):
    def city(name, prefix=None, legend_url=None, next_week=None, **canteens):
        city_definition = {
            'handler': parse_url,
            'prefix': prefix or 'http://www.stw-on.de/{}/essen/menus/mensa-'.format(name),
            'canteens': {k.replace('_', '-'): v for k, v in canteens.items()}
        }
        if legend_url:
            city_definition['options'] = {'legend_url': legend_url}
        if next_week is not None:
            city_definition.setdefault('options', {})
            city_definition['options']['next_week'] = next_week
        providers[name] = city_definition

    city('braunschweig',
         mensa1_mittag=('1', 'Mittagsmensa'),
         mensa1_abend=('1', 'Abendmensa'),
         mensa2='2',
         hbk='hbk',
         legend_url='http://www.stw-on.de/braunschweig/essen/wissenswertes/lebensmittelkennzeichnung')
    city('clausthal', clausthal='clausthal', next_week='-kommend-woche')
    city('hildesheim', prefix='http://www.stw-on.de/lueneburg/essen/menus/',
         uni='mensa-uni',
         hohnsen='mensa-hohnsen',
         luebecker_strasse=('luebecker-strasse', 'Mittagsausgabe'))
    city('holzminden', hawk='hawk', next_week=False)
    city('lueneburg', prefix='http://www.stw-on.de/lueneburg/essen/speiseplaene/',
         campus='mensa-campus',
         rotes_feld='rotes-feld')
    city('suderburg', suderburg='suderburg')
    city('wolfenbuettel', ostfalia='ostfalia')
