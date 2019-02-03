import re
import socket
from urllib.parse import urlparse, urlunparse, ParseResult
from urllib.request import Request, urlopen

from pyopenmensa.feed import LazyBuilder

from utils import Parser

day_regex = re.compile('(?P<date>\d{2}\.\d{2}\.\d{4})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2})€')
note_regex = re.compile('\((?P<number>[a-z0-9]+?)\)')
legend_regex = re.compile('\((?P<number>\w+)\) ?(?P<value>\w+(\s+\w+)*)')
meal_regex = re.compile('(?P<category>(\w|\s|\(|\))+):\s*(?P<meal>([^0-9\(]|[0-9]+(?!,))+)')

roles = ('student', 'employee', 'other')


def urlopen_via_ipv4(url):
    """ IPv6 request to www.stwh-portal.de timeout, so we
        disable them to skip the timeout.
        The easiest approach is to pass an IPv4 IP directly,
        there is no parameter to define the address family.
    """
    parts = urlparse(url)
    host = socket.gethostbyname(parts.netloc)
    newparts = ParseResult(scheme=parts.scheme,
                           netloc=host,
                           path=parts.path,
                           params=parts.params,
                           fragment=parts.fragment,
                           query=parts.query)
    request = Request(urlunparse(newparts),
                      headers={'Host': parts.netloc})
    return urlopen(request)


def parse_week(url, canteen):
    document = urlopen_via_ipv4(url).read().decode('utf8').split('\n')
    legends = {v.group('number'): v.group('value') for v in map(lambda v: legend_regex.match(v), document) if v}
    date = None
    for line in document:
        if not date:
            test = day_regex.search(line)
            if test:
                date = test.group('date')
            continue
        if 'geschlossen' in line.lower():
            canteen.setDayClosed(date)
        if not line.startswith('>'):
            date = None
            continue
        mealtest = meal_regex.search(line)
        if not mealtest:
            print('unable to parse category/meal: "{}"'.format(line))
            continue
        category = mealtest.group('category').strip()
        name = mealtest.group('meal').strip()
        notes = []
        for notematch in note_regex.findall(line):
            if notematch not in legends:
                print('unknown legend: {}'.format(notematch))
                continue
            notes.append(legends[notematch])
        canteen.addMeal(date, category, name, notes,
                        price_regex.findall(line)[-3:], roles)


def parse_url(url, today=False):
    canteen = LazyBuilder()
    parse_week(url + '&wann=2', canteen)
    if not today:
        parse_week(url + '&wann=3', canteen)
    return canteen.toXMLFeed()


parser = Parser('hannover', handler=parse_url,
                shared_prefix='http://www.stwh-portal.de/mensa/index.php?format=txt&wo=')
parser.define('hauptmensa', suffix='2')
parser.define('hauptmensa-marktstand', suffix='9')
parser.define('restaurant-ct', suffix='10')
parser.define('contine', suffix='3')
parser.define('pzh', suffix='13')
parser.define('caballus', suffix='1')
parser.define('tiho-tower', suffix='0')
parser.define('hmtmh', suffix='8')
parser.define('ricklinger-stadtweg', suffix='6')
parser.define('kurt-schwitters-forum', suffix='7')
parser.define('blumhardtstrasse', suffix='14')
parser.define('herrenhausen', suffix='12')
