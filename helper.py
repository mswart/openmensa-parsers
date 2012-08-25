import re
from xml.dom.minidom import Document
import datetime

date_format = re.compile(".*?(?P<datestr>(" +
				"\d{2}(\d{2})?-\d{2}-\d{2}|" +
				"\d{2}\.\d{2}\.\d{2}(\d{2})?|" +
				"(?P<day>\d{2})\. ?(?P<month>\w+) ?(?P<year>\d{2}(\d{2})?))).*")
month_names = {
	'Januar': '01',
	'Februar': '02',
	'März': '03',
	'April': '04',
	'Mai': '05',
	'Juni': '06',
	'Juli': '07',
	'August': '08',
	'September': '09',
	'Oktober': '10',
	'November': '11',
	'Dezember': '12'
}

def extractDate(text):
	match = date_format.search(text)
	if not match:
		raise ValueError('unsupported date format: DD.MM.YYYY, DD.MM.YY, YYYY-MM-DD, YY-MM-DD, DD. Month YYYY or DD. Month YY needed')
	# convert DD.MM.YYYY into YYYY-MM-DD
	if match.group('month'):
		if not match.group('month') in month_names:
			raise ValueError('unknown month names')
		year = int(match.group('year'))
		return datetime.date(
			year if year > 2000 else 2000 + year,
			int(month_names[match.group('month')]),
			int(match.group('day')))
	else:
		parts = list(map(lambda v : int(v), '-'.join(reversed(match.group('datestr').split('.'))).split('-')))
		if parts[0] < 2000: parts[0] += 2000
		return datetime.date(*parts)


class extractWeekDates():
	weekdaynames = {
		0: 0,
		'Mon': 0,
		'Montag': 0,
		'Dienstag': 1,
		'Mittwoch': 2,
		'Donnerstag': 3,
		'Freitag': 4,
		'Samstag': 5,
		'Sonntag': 6
	}
	def __init__(self, start, end=None):
		self.monday = extractDate(start)
	def __getitem__(self, value):
		if type(value) not in [int, str]:
			raise TypeError
		if value not in self.weekdaynames:
			raise ValueError
		return self.monday + datetime.date.resolution * self.weekdaynames[value]
	def __iter__(self):
		for i in range(7):
			yield self.monday + datetime.date.resolution * i


class OpenMensaCanteen():
	""" This class represents and stores all informations
		about OpenMensa canteens. It helps writing new
		python parsers with helper and shortcuts methods.
		So the complete object can be converted to a valid
		OpenMensa v2 xml feed string. """

	def __init__(self):
		""" Creates new instance and prepares interal data
			structures"""
		self._days = {}
		self.legendData = None
		self.additionalCharges = None

	default_legend_regex = '(?P<number>\d+)\)\s*(?P<value>\w+((\s+\w+)*[^0-9)]))'
	def setLegendData(self, text, legend_regex = default_legend_regex):
		self.legendData = {}
		for match in re.finditer(legend_regex, text):
			self.legendData[int(match.group('number'))] = match.group('value').strip()

	def setAdditionalCharges(self, defaultPriceRole, additionalCharges):
		""" This is a helper function, which fast up the calculation
			of prices. It is useable if the canteen has fixed
			additional charges for special roles.
			defaultPriceRole specifies for which price role the price
			of addMeal are.
			additionalCharges is a dictonary which defines the extra
			costs (value) for other roles (key)."""
		for role in additionalCharges:
			if type(additionalCharges[role]) is not float:
				additionalCharges[role] = float(additionalCharges[role].replace(',', '.'))
		self.additionalCharges = (defaultPriceRole, additionalCharges)

	def addMeal(self, date, category, name, notes = [],
			prices = {}, priceRoles = None):
		""" This is the main helper, it adds a meal to the
			canteen. The following data are needed:
			* date datestr: Date for the meal (see convertDate)
			* categor str: Name of the meal category
			* name str: Meal name
			Additional the following data are also supported:
			* notes list[]: List of notes (as List of strings)
			* prices {str: float}: Price of the meal; Every
			  key must be a string for the role of the persons
			  who can use this tariff; The value is the price in €,
			  as string. dot and comma are possible as decimal mark
			The site of the OpenMensa project offers more detailed
			information."""
		if type(date) is not datetime.date:
			date = extractDate(date)
		# ensure we have an entry for this date
		if date not in self._days:
			self._days[date] = {}
		# ensure we have a category element for this category
		if category not in self._days[date]:
			self._days[date][category] = []
		# handle notes:
		if notes is True:
			name, notes = self.extractNotes(name)
		# convert prices if needed:
		prices = self.buildPrices(prices, priceRoles)
		# add meal into category:
		self._days[date][category].append((name, notes, prices))

	def setDayClosed(self, date):
		""" Stores that this cateen is closed on $date."""
		self._days[extractDate(date)] = False

	def clearDay(self, date):
		try:
			del self._days[extractDate(date)]
		except KeyError:
			pass

	def dayCount(self):
		return len(self._days)

	def toXMLFeed(self):
		""" Convert this cateen information into string
			which is a valid OpenMensa v2 xml feed"""
		feed, document = self.createDocument()
		feed.appendChild(self.toTag(document))
		return '<?xml version="1.0" encoding="UTF-8"?>\n' + feed.toprettyxml(indent='  ')

	default_extra_regex = re.compile('\((?P<extra>[0-9,]+)\)')
	def extractNotes(self, name):
		if self.legendData is None:
			raise ValueError('setLegendData call needed!')
		# extract note
		notes = []
		for note in set(','.join(self.default_extra_regex.findall(name)).split(',')):
			if note and int(note) in self.legendData:
				notes.append(self.legendData[int(note)])
			elif note: # skip empty notes
				print('could not find extra note "{}"'.format(note))
		# from notes from name
		name = self.default_extra_regex.sub('', name).replace('\xa0',' ').replace('  ', ' ').strip()
		return name, notes

	price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')
	def buildPrices(self, data, roles):
		prices = {}
		if roles:
			priceRoles = iter(roles())
			for price in priceList:
				prices[next(priceRoles)] = price
		elif type(data) is str:
			if self.additionalCharges is None:
				raise ValueError('You have to call setAdditionalCharges before it is possible to pass a string as price')
			match = self.price_regex.search(data)
			if not match:
				raise ValueError('Could not extract price from given string: "{}"'.format(data))
			price = float(match.group('price').replace(',', '.'))
			prices = {
				self.additionalCharges[0]: '{:.2f}'.format(price),
			}
			for role in self.additionalCharges[1]:
				prices[role] = '{:.2f}'.format(price + self.additionalCharges[1][role])
		elif type(data) is dict:
			prices = data
		else:
			raise TypeError('This type is for prices not supported!')
		return prices

	@staticmethod
	def createDocument():
		# create xml document
		output = Document()
		# build main openmensa element with correct xml namespaces
		openmensa = output.createElement('openmensa')
		openmensa.setAttribute('version', '2.0')
		openmensa.setAttribute('xmlns', 'http://openmensa.org/open-mensa-v2')
		openmensa.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
		openmensa.setAttribute('xsi:schemaLocation', 'http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd')
		return openmensa, output

	def toTag(self, output):
		# create canteen tag, which represents our data
		canteen = output.createElement('canteen')
		# iterate above all days (sorted):
		for date in sorted(self._days.keys()):
			day = output.createElement('day')
			day.setAttribute('date', str(date))
			if self._days[date] is False: # canteen closed
				closed = output.createElement('closed')
				day.appendChild(closed)
				canteen.appendChild(day)
				continue
			# canteen is open
			for categoryname in self._days[date]:
				day.appendChild(self.buildCategoryTag(
					categoryname, self._days[date][categoryname], output))
			canteen.appendChild(day)
		return canteen

	@classmethod
	def buildCategoryTag(cls, name, data, output):
		# skip empty categories:
		if len(data) < 1:
			return None
		category = output.createElement('category')
		category.setAttribute('name', name)
		for meal in data:
			category.appendChild(cls.buildMealTag(meal, output))
		return category

	@classmethod
	def buildMealTag(cls, mealData, output):
		name, notes, prices = mealData
		meal = output.createElement('meal')
		# add name
		nametag = output.createElement('name')
		nametag.appendChild(output.createTextNode(name))
		meal.appendChild(nametag)
		# add notes:
		for note in notes:
			notetag = output.createElement('note')
			notetag.appendChild(output.createTextNode(note))
			meal.appendChild(notetag)
		# add prices:
		for role in prices:
			price = output.createElement('price')
			price.setAttribute('role', role)
			price.appendChild(output.createTextNode(prices[role].strip().replace(',', '.')))
			meal.appendChild(price)
		return meal
