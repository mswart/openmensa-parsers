#!python3
from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime

from pyopenmensa.feed import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{2}\.\d{2}\.\d{4})')
day_range_regex = re.compile('(?P<from>\d{2}\.\d{2}\.\d{4}).* (?P<to>\d{2}\.\d{2}\.\d{4})')
extra_regex = re.compile('\((?P<number>\d+)\)')
legend_regex = re.compile('(?P<number>\d+)\) (?P<value>\w+(\s+\w+)*)')

def rolesGenerator():
	yield 'student'
	yield 'employee'
	while True:
		yield 'other'

def parse_url(url):
	content = urlopen(url).read()
	document = parse(content)
	legends = document.find_all('div', {'class':'legende'})
	if len(legends) > 0:
		extraLegend = { int(v[0]): v[1] for v in reversed(legend_regex.findall(legends[0].text)) }
	else:
		extraLegend = {}
	canteen = OpenMensaCanteen()
	for day_td in document.find_all('td', text = day_regex):
		date = day_regex.search(day_td.string).group('date')
		table = None
		for element in day_td.parents:
			if element.name == 'table':
				table = element
				break
		if not table: continue
		for tr in table.tbody.find_all('tr'):
			if 'geschlossen' in tr.text or 'Feiertage' in tr.text:
				match = day_range_regex.search(tr.text)
				if not match:
					canteen.setDayClosed(date)
				else:
					fromDate = datetime.datetime.strptime(match.group('from'), '%d.%m.%Y')
					toDate = datetime.datetime.strptime(match.group('to'), '%d.%m.%Y')
					while fromDate <= toDate:
						canteen.setDayClosed(fromDate.strftime('%Y-%m-%d'))
						fromDate += datetime.date.resolution
				continue
			if len(tr) != 3 : continue # no meal
			strings = list(tr.contents[0].strings)
			name = strings[0]
			# notes:
			notes = []
			for img in tr.contents[1].find_all('img'):
				notes.append(img['alt'].replace('Symbol', '').strip())
			for extra in list(set(map(lambda v: int(v), extra_regex.findall(tr.text)))):
				if extra in extraLegend:
					notes.append(extraLegend[extra])
			canteen.addMeal(date, 'Hauptgerichte', name, notes,
				strings[-1].split('|'), rolesGenerator)
	return canteen.toXMLFeed()
