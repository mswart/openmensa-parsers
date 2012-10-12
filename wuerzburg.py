#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from helper import OpenMensaCanteen

day_regex = re.compile('(?P<day>\d{2})\.(?P<month>\d{2})\.')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
extra_regex = re.compile('[0-9,]+=(?P<note>\w+(\s|\w)*)')

def parse_url(url):
	canteen = OpenMensaCanteen()
	document = parse(urlopen(url).read())
	for day_div in document.find_all('div', 'day') + document.find_all('article', attrs={'data-day': True}):
		# parse date, warning: calculate year number needed
		date_test = day_regex.search(day_div['data-day'])
		if not date_test:
			print('Error: unable to parse date')
			continue
		else:
			year = datetime.datetime.now().year
			if datetime.datetime.now().month > int(date_test.group('month')):
				year += 1 # date from next year
			date = "{}-{}-{}".format(year, date_test.group('month'), date_test.group('day'), )
		if 'nodata' in day_div.attrs.get('class', []) or 'GESCHLOSSEN' in day_div.text:
			canteen.setDayClosed(date)
			continue
		for meal_article in day_div.find_all('article', 'menu'):
			name = meal_article.find('div', 'title').text
			if not name:
				continue
			category = meal_article.find('div', 'desc').text
			notes = [ v['title'] for v in meal_article.find_all('div', 'theicon') if v['title'] ]
			if meal_article.find('div', 'additive'):
				notes += [ v[0] for v in extra_regex.findall(meal_article.find('div', 'additive').text) ]
			price_div = meal_article.find('div', 'price')
			prices = {}
			for v, r in ( ('default', 'student'), ('bed', 'employee'), ('guest', 'other') ):
				price = price_regex.search(price_div['data-' + v])
				if price:
					prices[r] = price.group('price')
				elif v == 'default':
					prices = False
					canteen.setDayClosed(date)
					break
			if prices and name:
				canteen.addMeal(date, category, name, notes, prices)
	return canteen.toXMLFeed()
