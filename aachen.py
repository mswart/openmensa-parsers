#!python3
from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup as parse
import re
import datetime

from helper import OpenMensaCanteen

day_regex = re.compile('(?P<date>\d{2}\. ?\d{2}\. ?\d{4})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
extra_regex = re.compile('\((?P<extra>[0-9,]+)\)')
legend_regex = re.compile('\((\d+)\) (\w+(\s|\w)*)')

def rolesGenerator():
	yield 'student'
	yield 'employee'

def parse_week(url, data, canteen):
	document = parse(urlopen(url, data).read())
	# parse extra/notes legend
	legends = {}
	legendsData = document.find('table', 'zusatz_std')
	if legendsData:
		legends = { int(v[0]): v[1] for v in legend_regex.findall(legendsData.text.replace('\xa0',' ')) }
	# iterator about all rows of the table
	rowIter = iter(document.find('table', 'wo_std').find_all('tr'))
	# extra category names fro th's of first row
	categories = list(map(lambda v: v.text.strip(), next(rowIter).find_all('th')))[1:]
	try:
		while True:
			tr = next(rowIter) # meal row
			extratr = next(rowIter) # addition meal component row, ToDo
			# extract date from first column:
			date = day_regex.search(tr.contents[0].text).group('date')
			# build iterators for lists:
			categoriesIterator = iter(categories)
			colIter = iter(tr.find_all('td'))
			extraIter = iter(extratr.find_all('td'))
			# skip first row (date):
			next(colIter)
			next(extraIter)
			try:
				while True:
					name = next(colIter).text
					# extract notes from name
					notes = [ legends[int(v)] for v in set(','.join(extra_regex.findall(name)).split(',')) if v and int(v) in legends ]
					# from notes from name
					name = extra_regex.sub('', name).replace('\xa0',' ').replace('  ', ' ').strip()
					# extract price
					price = float(price_regex.search(v).group('price').replace(',', '.'))
					prices = {
						'students': str(price),
						'other': str(price + 1.5)
					}
					canteen.addMeal(date, next(categoriesIterator), name, notes, prices)
			except StopIteration:
				pass
	except StopIteration:
		pass

def parse_url(url):
	canteen = OpenMensaCanteen()
	document = parse(urlopen(url).read())
	for submit in document.find_all('input'):
		if submit['type'] != 'submit': continue
		parse_week(url, urlencode({ submit['name']: submit['value']}).encode('utf8'), canteen)
	return canteen.toXMLFeed()
