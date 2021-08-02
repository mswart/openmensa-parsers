from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from utils import EasySource, Parser, Source
from datetime import timedelta, date
from pyopenmensa.feed import LazyBuilder
import ssl


# matches two digit prices such as 1,23 or 23,41 (hoping for low inflation)
price_regex = re.compile(r'\d{1,2},\d{1,2}')
# matches a digit or a letter followed by a digit between whitespace and comma, comma and comma or comma and whitespace
additives_regex = re.compile(r'(?<=\s)\S?\d(?=,)|(?<=,)\S?\d(?=,)|(?<=,)\S?\d(?=\s)')
# matches two or three character blocks
allergens_regex = re.compile(r'(?<=\s)\w{2,3}(?=,)|(?<=,)\w{2,3}(?=,)|(?<=,)\w{2,3}(?=\s)')

def parse_meals(document):
	meals = document.find_all(class_='rowMealInner')
	for meal in meals:
		name = meal.find_next(class_='mealText').string.strip()

		additives_string = meal.find_next(class_='zusatzstoffe').string
		allergens_string = meal.find_next(class_='allergene').string

		misc = []
		for misc_category in meal.find_all(class_='splIconMeal'):
			misc.append(misc_category['title'])
			
		info = {
				'additives': additives_regex.findall(additives_string) if additives_string else [],
				'allergens': allergens_regex.findall(allergens_string) if allergens_string else [],
				'misc': misc
		}
		prices = price_regex.findall(meal.find_next(class_='mealPreise').string)
		yield (name, info, prices)


# matches legend labels
legend_item_regex = re.compile(r'stoff-.{1,3}')
# get legend key and value omitting 'mit' and 'enthält'
legend_key_val_regex = re.compile(r'\((?P<key>\S{1,3})\) (?:(?:mit )|(?:enthält ))?(?P<value>.*)')

def parse_legend(document):
	legend = {}
	for item in document.find_all('label', attrs={'for': legend_item_regex}):
		# is a shortcut with key in parenthesis
		if match := legend_key_val_regex.search(item.string):
			(key, value) = match.group('key', 'value')
			legend[key] = value
	return legend

def parse_closed(document):
	return bool(document.find_all('h2', string='Zum gewählten Datum werden in dieser Einrichtung keine Essen angeboten.'))

class Canteen(EasySource):
	ENDPOINT_URL = 'https://www.stw-thueringen.de/xhr/loadspeiseplan.html'

	def __init__(self, *args, canteen_id):
		super().__init__(*args)
		self.canteen_id = canteen_id

		# www.stw-thueringen.de is currently not providing the intermediate
		# cert in its chain, so we just disable any cert checking, see:
		# https://github.com/mswart/openmensa-parsers/issues/109
		self.tls_context = ssl.create_default_context()
		self.tls_context.check_hostname = False
		self.tls_context.verify_mode = ssl.CERT_NONE

	def parse_single_date(self, date):
		post_args = [
			('resources_id', self.canteen_id),
			('date', date.strftime('%d.%m.%Y'))
		]
		print('fetching date ' + post_args[1][1])
		document = self.parse_remote(self.ENDPOINT_URL, args=post_args, tls_context=self.tls_context)
		if not parse_closed(document):
			legend = parse_legend(document)
			for (name, info, prices) in parse_meals(document):
				# determine category (Vegan, Vegetarisch, Fisch, Fleisch)
				category = 'Fleisch'
				if 'Vegane Speisen' in info['misc']:
					category = 'Vegan'
				elif 'Vegetarische Speisen' in info['misc']:
					category = 'Vegetarisch'
				elif 'Fisch' in info['misc']:
					category = 'Fisch'

				additives = 'Zusatzstoffe: ' + (', '.join((legend[item] for item in info['additives'])) if info['additives'] else 'keine')
				allergens = 'Allergene: ' + (', '.join((legend[item] for item in info['allergens'])) if info['allergens'] else 'keine')
				# remove information which is already present in the category
				misc = ', '.join((item for item in info['misc'] if item not in ['Vegane Speisen', 'Vegetarische Speisen', 'Fisch']))

				print(category)
				print(name)
				print(additives)
				print(allergens)
				print(misc)
				print(prices)
				print('-----')
				notes = [additives, allergens]
				# only add misc if not empty
				if len(misc):
					notes.append(misc)

				self.feed.addMeal(date, category, name, notes=notes, prices=prices, roles=('student', 'employee', 'other'))
			return True
		else:
			return False

	def parse_data(self, start_date, today=False):
		not_available_count = 0
		
		# ignore weekends
		while not_available_count <= 2:
			if self.parse_single_date(start_date):
				not_available_count = 0
			else:
				# no meals available
				not_available_count += 1
			# only fetch a single day
			if today:
				break
			# increment day
			start_date += timedelta(days=1)

		print('--------------------------')

	def extract_metadata(self):
		city = self.suffix.split('/')[0]
		doc = self.parse_remote(self.BASE_URL + city, tls_context=self.tls_context)
		data = doc.find(id='tpl_form')

		# The map this data was intended for was removed along with
		# all data, so this will always be None currently.
		if data is None:
			return

		link = data.find(attrs={
			'name': re.compile(r'^link_'),
			'value': re.compile(r'{}$'.format(re.escape(self.suffix))),
		})
		if link is None:
			return

		number = link['name'][5:]
		name = data.find(attrs={'name': 'title_' + number})['value']
		address = data.find(attrs={'name': 'adresse_' + number})['value']
		location = data.find(attrs={'name': 'xy_' + number})['value']

		canteen = self.feed
		canteen.name = name
		canteen.address = re.sub(r'^(.*)\s+([^\s]+)\s+(\d{5})\s*$', r'\1, \3 \2', address)
		canteen.city = city.capitalize()
		canteen.location(*location.split(','))

	@Source.today_feed
	def today(self, request):
		day = date.today()
		self.parse_data(day, True)
		return self.feed.toXMLFeed()

	@Source.full_feed
	def full(self, request):
		day = date.today()
		self.parse_data(day, False)
		return self.feed.toXMLFeed()

parser = Parser('thueringen', version='2.0')
#Canteen('ei-wartenberg', parser, suffix='eisenach/mensa-am-wartenberg-2.html')
#Canteen('ef-nordhaeuser', parser, suffix='erfurt/mensa-nordhaeuser-strasse.html')
#Canteen('ef-altonaer', parser, suffix='erfurt/mensa-altonaer-strasse.html')
#Canteen('ef-schlueterstr', parser, suffix='erfurt/cafeteria-schlueterstrasse.html')
#Canteen('ef-leipzigerstr', parser, suffix='erfurt/cafeteria-leipziger-strasse.html')
#Canteen('ge-freundschaft', parser, suffix='gera/mensa-weg-der-freundschaft.html')
#Canteen('il-ehrenberg', parser, suffix='ilmenau/mensa-ehrenberg.html')
#Canteen('il-cafeteria', parser, suffix='ilmenau/cafeteria-mensa-ehrenberg.html')
#Canteen('il-nanoteria', parser, suffix='ilmenau/cafeteria-nanoteria.html')
#Canteen('il-roentgen', parser, suffix='ilmenau/cafeteria-roentgenbau.html')
#Canteen('je-zeiss', parser, suffix='jena/mensa-carl-zeiss-promenade.html')
#Canteen('je-eah', parser, suffix='jena/cafeteria-eah.html')
#Canteen('je-ernstabbe', parser, suffix='jena/mensa-ernst-abbe-platz.html')
#Canteen('je-vegeTable', parser, suffix='jena/vegetable.html')
#Canteen('je-rosen', parser, suffix='jena/cafeteria-zur-rosen.html')
Canteen('je-philosophen', parser, canteen_id=59)
#Canteen('je-haupt', parser, suffix='jena/cafeteria-uni-hauptgebaeude.html')
#Canteen('je-bib', parser, suffix='jena/cafeteria-bibliothek-thulb.html')
#Canteen('nh-mensa', parser, suffix='nordhausen/mensa-nordhausen.html')
#Canteen('sk-mensa', parser, suffix='schmalkalden/mensa-schmalkalden.html')
#Canteen('we-horn', parser, suffix='weimar/cafeteria-am-horn.html')
#Canteen('we-park', parser, suffix='weimar/mensa-am-park.html')
#Canteen('we-anna', parser, suffix='weimar/cafeteria-anna-amalia-bibliothek.html')
#Canteen('we-coudray', parser, suffix='weimar/cafeteria-coudraystrasse.html')
