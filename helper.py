import re
from xml.dom.minidom import Document


class OpenMensaCanteen():
	""" This class represents and stores all informations
		about OpenMensa canteens. It helps writing new
		python parsers with helper and shortcuts methods.
		So the complete object can be converted to a valid
		OpenMensa v2 xml feed string. """

	# regex to parse and validate date formats:
	date_format = re.compile("^(\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4})$")


	def __init__(self):
		""" Creates new instance and prepares interal data
			structures"""
		self._days = {}


	# helper
	@classmethod
	def convertDate(cls, datestr):
		""" helper to convert all often date str into
			OpenMensa format (YYYY-MM-DD).
			Currently only DD.MM.YYYY is supported additional."""
		match = cls.date_format.match(datestr)
		if not match:
			raise ValueError('unsupported date format: DD.MM.YYYY or YYYY-MM-DD')
		# convert DD.MM.YYYY into YYYY-MM-DD
		return '-'.join(reversed(datestr.split('.')))


	def addMeal(self, date, category, name, notes = [], prices = {}):
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
			The site of the OpenMensa projects offers more detailed
			information."""
		date = self.convertDate(date) # ensure correct date format
		# ensure we have an entry for this date
		if date not in self._days:
			self._days[date] = []
		# ensure we have a category element for this category
		if category not in self._days[category]:
			self._days[category] = category
		# add meal into category:
		self._days[category].append((name, notes, prices))

	def setDayClosed(self, date):
		""" Stores that this cateen is closed on $date."""
		self._days[self.convertDate(date)] = False

	def toXMLFeed(self):
		""" Convert this cateen information into string
			which is a valid OpenMensa v2 xml feed"""
		# create xml document
		output = Document()
		# build main openmensa element with correct xml namespaces
		openmensa = output.createElement('openmensa')
		openmensa.setAttribute('version', '2.0')
		openmensa.setAttribute('xmlns', 'http://openmensa.org/open-mensa-v2')
		openmensa.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
		openmensa.setAttribute('xsi:schemaLocation', 'http://openmensa.org/open-mensa-v2 http://openmensa.org/open-mensa-v2.xsd')
		# create canteen tag, which represents our data
		canteen = output.createElement('canteen')
		openmensa.appendChild(canteen)
		# iterate above all days (sorted):
		for date in sorted(self._days.keys()):
			day = output.createElement('day')
			day.setAttribute('date', date)
			if self._days[date] is False: # canteen closed
				closed = output.createElement('closed')
				day.appendChild(closed)
				canteen.appendChild(day)
				continue
			# canteen is open
			haveCategoriesWithMeal = False # don't add days without content
			for categoryname in self._days[date]:
				# skip empty categories:
				if len(self._days[date][categoryname]) < 1:
					continue
				category = output.createElement('category')
				category.setAttribute('name', categoryname)
				for name, notes, prices in self._days[categoryname]:
					meal = output.createElement('meal')
					# add name
					nametag = output.createElement('name')
					nametag.appendChild(document.createTextNode(name))
					meal.appendChild(nametag)
					# add notes:
					for note in notes:
						notetag = output.createElement('note')
						notetag.appendChild(document.createTextNode(note))
						meal.appendChild(notetag)
					# add prices:
					for role in prices:
						price = output.createElement('price')
						price.setAttribute('role', role)
						price.appendChild(document.createTextNode(prices[price]))
						meal.appendChild(price)
					category.appendChild(meal)
				haveCategoriesWithMeal = True
				day.appendChild(category)
			if haveCategoriesWithMeal:
				canteen.appendChild(day)

