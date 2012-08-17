#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from xml.dom.minidom import Document

day_regex = re.compile('(?P<date>\d{4}-\d{2}-\d{2})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')

def rolesGenerator():
	yield 'student'
	yield 'other'
	yield 'employee'
	while True:
		yield 'other'


def parse_url(url, place_class=None):
	content = urlopen(url).read()
	document = parse(content)
	legends = document.find_all('div', {'class':'legende'})
	if len(legends) > 0:
		extraLegend = { int(v[0]): v[1] for v in reversed(legend_regex.findall(legends[0].text)) }
	else:
		extraLegend = {}
	output = Document()
	openmensa = output.createElement('openmensa')
	openmensa.setAttribute('version', '2.0')
	openmensa.setAttribute('xmlns',"http://openmensa.org/open-mensa-v2")
	openmensa.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
	openmensa.setAttribute('xsi:schemaLocation', "http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd")
	output.appendChild(openmensa)
	canteen = output.createElement('canteen')
	openmensa.appendChild(canteen)

	if place_class:
		document = document.find(id=place_class)

	for day_a in document.find_all('a', rel = day_regex):
		day_data = document.find(id=day_a['href'].replace('#', ''))
		if not day_data: continue
		day = output.createElement('day')
		print(day_a['rel'])
		day.setAttribute('date', day_a['rel'][0])
		day_table = day_data.table
		if not day_table: continue
		if day_table.tbody: day_table = day_table.tbody
		for category_tr in day_table.children:
			if category_tr.name != 'tr': continue
			if len(category_tr) < 2 : continue # no meal
			category = output.createElement('category')
			category.setAttribute('name', category_tr.contents[0].text)
			meal_table = category_tr.contents[1].table
			if meal_table.tbody: meal_table = meal_table.tbody
			for meal_tr in meal_table.children:
				if meal_tr.name != 'tr': continue
				if len(list(meal_tr.children)) != 3:
					print('skipping category, unable to parse meal_table: {} tds'.format(len(list(meal_tr.children))))
					continue
				meal = output.createElement('meal')
				name = output.createElement('name')
				name.appendChild(output.createTextNode(meal_tr.contents[1].text))
				meal.appendChild(name)
				# notes, to do
				# prices:
				priceRoles = iter(rolesGenerator())
				for pricematch in price_regex.findall(meal_tr.contents[2].text):
					price = output.createElement('price')
					price.setAttribute('role', next(priceRoles))
					price.appendChild(output.createTextNode(pricematch.strip().replace(',', '.')))
					meal.appendChild(price)
				category.appendChild(meal)
			day.appendChild(category)
		canteen.appendChild(day)
	return '<?xml version="1.0" encoding="UTF-8"?>\n' + openmensa.toprettyxml(indent='  ')
