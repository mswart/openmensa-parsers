import re
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse

from utils import Parser

from pyopenmensa.feed import LazyBuilder, extractDate, buildLegend


def parse_week(url, canteen, type, allergene={}, zusatzstoffe={}):
    document = parse(urlopen(url).read(), 'lxml')
    for day_table in document.find_all('table', 'swbs_speiseplan'):
        caption = day_table.find('th', 'swbs_speiseplan_head').text
        if type not in caption:
            continue
        date = extractDate(caption)
        meals = day_table.find_all('tr')
        pos = 0
        while pos < len(meals):
            meal_tr = meals[pos]
            if not meal_tr.find('td'):  # z.B Headline
                pos += 1
                continue
            tds = meal_tr.find_all('td')
            category = re.sub(r' \(\d\)', '', tds[0].text.strip())
            name = tds[1].text.strip()
            if tds[1].find('a', href='http://www.stw-on.de/mensavital'):
                notes = ['MensaVital']
            else:
                notes = []
            for img in tds[2].find_all('img'):
                title = img['title']
                if ':' in title:
                    kind, value = title.split(':')
                    if kind == 'Allergene':
                        for allergen in value.split(','):
                            notes.append(allergene.get(allergen.strip()) or allergene[allergen.strip()[:-1]])
                    elif kind == 'Zusatzstoffe':
                        for zusatzstoff in value.split(','):
                            notes.append(zusatzstoffe[zusatzstoff.strip()])
                    else:
                        print('Unknown image type "{}"'.format(kind))
                else:
                    notes.append(title.replace('enthält ', ''))
            prices = {
                'student':  tds[3].text.strip(),
                'employee': tds[4].text.strip(),
                'other':    tds[5].text.strip()
            }
            if pos < len(meals) - 1:
                nextTds = meals[pos+1].find_all('td')
                if nextTds[0].text.strip() == '':
                    pos += 1
                    for img in nextTds[1].find_all('img'):
                        notes.append(img['title'])
            pos += 1
            canteen.addMeal(date, category, name, notes, prices)


def parse_url(url, today=False, canteentype='Mittagsmensa', this_week='', next_week=True, legend_url=None):
    canteen = LazyBuilder()
    canteen.legendKeyFunc = lambda v: v.lower()
    if not legend_url:
        legend_url = url[:url.find('essen/') + 6] + 'wissenswertes/lebensmittelkennzeichnung'
    legend_doc = parse(urlopen(legend_url), 'lxml').find(id='artikel')
    allergene = buildLegend(
        text=legend_doc.text.replace('\xa0', ' '),
        regex=r'(?P<name>[A-Z]+) {3,}enthält (?P<value>\w+( |\t|\w)*)'
    )
    allergene['EI'] = 'Ei'
    zusatzstoffe = buildLegend(
        text=legend_doc.text.replace('\xa0', ' '),
        regex=r'(?P<name>\d+) {3,} (enthält )?(?P<value>\w+( |\t|\w)*)'
    )
    suballergene = re.compile(r'(?P<name>[0-9A-Z]+)[^a-zA-Z]*enthält (?P<value>\w+( |\t|\w)*)')
    for tr in legend_doc.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) != 2:
            continue
        title = tds[0].find('strong')
        if title is None:
            continue
        else:
            title = title.text
        lines = tds[1].text.split('\n')
        for line in lines[1:]:
            try_allergine = suballergene.match(line)
            if try_allergine:
                allergene[try_allergine.group('name')] = try_allergine.group('value')
        text = lines[0].replace('enthält', '').strip()
        if title.isdigit():
            zusatzstoffe[title] = text
        else:
            allergene[title] = text
    parse_week(url + this_week, canteen, canteentype,
               allergene=allergene, zusatzstoffe=zusatzstoffe)
    if not today and next_week is True:
        parse_week(url + '-kommende-woche', canteen, canteentype,
                   allergene=allergene, zusatzstoffe=zusatzstoffe)
    if not today and type(next_week) is str:
        parse_week(url + next_week, canteen, canteentype,
                   allergene=allergene, zusatzstoffe=zusatzstoffe)
    return canteen.toXMLFeed()


parser = Parser('ostniedersachsen', handler=parse_url,
                shared_prefix='http://www.stw-on.de')

sub = parser.sub('braunschweig',
                 shared_prefix='/braunschweig/essen/menus/')
sub.define('mensa1-mittag', suffix='mensa-1', extra_args={'canteentype': 'Mittagsmensa'})
sub.define('mensa1-abend', suffix='mensa-1', extra_args={'canteentype': 'Abendmensa'})
sub.define('mensa360', suffix='360', extra_args={'canteentype': 'Pizza', 'this_week': '-2', 'next_week': '-nachste-woche'})
sub.define('mensa2', suffix='mensa-2')
sub.define('hbk', suffix='mensa-hbk')

parser.define('clausthal', suffix='/clausthal/essen/menus/mensa-clausthal',
              extra_args={'next_week': '-kommend-woche'})

sub = parser.sub('hildesheim', shared_prefix='/hildesheim/essen/menus/')
sub.define('uni', suffix='mensa-uni')
sub.define('hohnsen', suffix='mensa-hohnsen')
sub.define('luebecker-strasse', suffix='luebecker-strasse', extra_args={'canteentype': 'Mittagsausgabe'})

parser.sub('suderburg').define('campus', suffix='/suderburg/essen/menus/mensa-suderburg')
parser.sub('wolfenbuettel').define('ostfalia', suffix='/wolfenbuettel/essen/menus/mensa-ostfalia')
parser.sub('holzminden', shared_prefix='/holzminden/essen/menus/') \
    .define('hawk', suffix='mensa-hawk', extra_args={'next_week': False})

sub = parser.sub('lueneburg', shared_prefix='/lueneburg/essen/speiseplaene/')
sub.define('campus', suffix='mensa-campus')
sub.define('rotes-feld', suffix='rotes-feld')
