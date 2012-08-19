#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from helper import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{2}\. ?\w+ ?\d{4})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')

def rolesGenerator():
	yield 'student'
	yield 'employee'

def parse_week(url, canteen):
	document = parse(urlopen(url).read())
	for day_table in document.find_all('table', 'speiseplan'):
		date = day_regex.search(day_table.thead.tr.th.text).group('date')
		if day_table.find('td', 'keinangebot'):
			canteen.setDayClosed(date)
			continue
		for meal_tr in day_table.tbody.children:
			name = meal_tr.td.text
			if ':' in name:
				category, name = name.split(': ', 1)
			else:
				category = 'Angebote'
			notes = []
			for img in meal_tr.find_all('img'):
				notes.append(img['title'])
			canteen.addMeal(date, category, name, notes,
				price_regex.findall(meal_tr.text), rolesGenerator)

def parse_url(url):
	canteen = OpenMensaCanteen()
	parse_week(url + '.html', canteen)
	parse_week(url + '-w1.html', canteen)
	parse_week(url + '-w2.html', canteen)
	return canteen.toXMLFeed()
