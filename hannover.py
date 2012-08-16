#!python3
from urllib.request import urlopen
import re
from xml.dom.minidom import Document

day_regex = re.compile('(?P<date>\d{2}\.\d{2}\.\d{4})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2})€')
note_regex = re.compile('\((?P<number>[a-z0-9]+?)\)')
legend_regex = re.compile('\((?P<number>\w+)\) ?(?P<value>\w+(\s+\w+)*)')
meal_regex = re.compile('(?P<category>(\w|\s|\(|\))+):\s*(?P<meal>(\w|\s)+)')

def rolesGenerator():
	yield 'student'
	yield 'employee'
	while True:
		yield 'other'

def parse_week(url, canteen, output):
	document = urlopen(url).read().decode('utf8').split('\n')
	legends = { v.group('number'): v.group('value') for v in filter(lambda d: d, map(lambda v: legend_regex.match(v), document))}
	date = None
	day = None
	for line in document:
		if not date:
			test = day_regex.search(line)
			if not test:
				continue
			else:
				date = test.group('date')
				day = output.createElement('day')
				day.setAttribute('date', '{}-{}-{}'.format(date[6:10], date[3:5], date[0:2]))
				continue
		if not line.startswith('>'):
			if day:
				canteen.appendChild(day)
			date = None
			continue
		mealtest = meal_regex.search(line)
		if not mealtest:
			print('unable to parse category/meal: "{}"'.format(line))
			continue
		category = output.createElement('category')
		category.setAttribute('name', mealtest.group('category').strip())
		meal = output.createElement('meal')
		name = output.createElement('name')
		name.appendChild(output.createTextNode(mealtest.group('meal').strip()))
		meal.appendChild(name)
		for notematch in note_regex.findall(line):
			if notematch not in legends: 
				print('unknown legend: {}'.format(notematch))
				continue
			note = output.createElement('note')
			note.appendChild(output.createTextNode(legends[notematch]))
			meal.appendChild(note)
		priceRoles = iter(rolesGenerator())
		for pricematch in price_regex.findall(line):
			price = output.createElement('price')
			price.setAttribute('role', next(priceRoles))
			price.appendChild(output.createTextNode(pricematch.strip().replace(',', '.')))
			meal.appendChild(price)
		category.appendChild(meal)
		day.appendChild(category)

def parse_url(url):
	output = Document()
	openmensa = output.createElement('openmensa')
	openmensa.setAttribute('version', '2.0')
	openmensa.setAttribute('xmlns',"http://openmensa.org/open-mensa-v2")
	openmensa.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
	openmensa.setAttribute('xsi:schemaLocation', "http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd")
	output.appendChild(openmensa)
	canteen = output.createElement('canteen')
	openmensa.appendChild(canteen)
	parse_week(url + '&wann=2', canteen, output)
	parse_week(url + '&wann=3', canteen, output)
	return '<?xml version="1.0" encoding="UTF-8"?>\n' + openmensa.toprettyxml(indent='  ')
