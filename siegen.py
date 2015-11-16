from bs4 import BeautifulSoup
from pyopenmensa.feed import LazyBuilder
from urllib.request import urlopen
from utils import Parser

def parse_week(url, canteen):
    soup = BeautifulSoup(urlopen(url).read(), 'lxml')
    plan_table = soup.find("table", "tabmensaplan")
    for day_span in plan_table.find_all("span", "tabDate"):
        meal_date = day_span.text + "2015"
        for index, meal_td in enumerate(day_span.parent.parent.find_all("td")):
            if index > 0 and index < 5:
                meal_text = meal_td.text
                meal_type = soup.find_all("span", "mvmensa")[index-1].text
                canteen.addMeal(meal_date, meal_type, meal_text)

def parse_url(url, today):
    canteen = LazyBuilder()
    if not today:
        parse_week(url, canteen)
    return canteen.toXMLFeed()

parser = Parser('siegen', handler=parse_url,
    shared_prefix='http://studentenwerk.uni-siegen.de/index.php?uid=650&uid2=0')
parser.define('ar', suffix='&cat_show=1')
parser.define('enc', suffix='&cat_show=2')
parser.define('ars-mundi', suffix='&cat_show=3')
parser.define('cafeterien', suffix='&cat_show=4')
