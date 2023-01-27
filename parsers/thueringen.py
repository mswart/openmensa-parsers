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

		additives_element = meal.find_next(class_='zusatzstoffe')
		allergens_element = meal.find_next(class_='allergene')

		misc = []
		for misc_category in meal.find_all(class_='splIconMeal'):
			misc.append(misc_category['title'])
			
		info = {
				'additives': additives_regex.findall(additives_element.string) if additives_element and additives_element.string else [],
				'allergens': allergens_regex.findall(allergens_element.string) if allergens_element and allergens_element.string else [],
				'misc': misc
		}
		prices_element = meal.find_next(class_='mealPreise')
		prices = price_regex.findall(prices_element.string) if prices_element else None
		
		# check for non-empty name
		if len(name):
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

	def parse_single_date(self, date):
		post_args = [
			('resources_id', self.canteen_id),
			('date', date.strftime('%d.%m.%Y'))
		]
		document = self.parse_remote(self.ENDPOINT_URL, args=post_args)
		if not parse_closed(document):
			legend = parse_legend(document)
			for (name, info, prices) in parse_meals(document):
				# determine category (Vegan, Vegetarisch, Fisch, Fleisch)
				category = 'Fleisch'
				if 'Vegane Speisen (V*)' in info['misc']:
					category = 'Vegan'
				elif 'Vegetarische Speisen (V)' in info['misc']:
					category = 'Vegetarisch'
				elif 'Fisch (F)' in info['misc']:
					category = 'Fisch'

				additives = 'Zusatzstoffe: ' + ', '.join((legend[item] for item in info['additives'])) if info['additives'] else 'ohne deklarationspflichtige Zusatzstoffe'
				allergens = 'Allergene: ' + ', '.join((legend[item] for item in info['allergens'])) if info['allergens'] else ''
				# remove information which is already present in the category
				misc = ', '.join((item for item in info['misc'] if item not in ['Vegane Speisen', 'Vegetarische Speisen', 'Fisch']))

				notes = [additives]
				# only add misc and allergens if not empty
				if len(allergens):
					notes.append(allergens)
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
Canteen('ei-wartenberg', parser, canteen_id=69)
Canteen('ef-nordhaeuser', parser, canteen_id=44)
Canteen('ef-altonaer', parser, canteen_id=47)
Canteen('ef-schlueterstr', parser, canteen_id=51)
Canteen('ef-leipzigerstr', parser, canteen_id=52)
Canteen('ge-freundschaft', parser, canteen_id=67)
Canteen('il-ehrenberg', parser, canteen_id=46)
Canteen('il-cafeteria', parser, canteen_id=53)
Canteen('il-nanoteria', parser, canteen_id=55)
Canteen('il-roentgen', parser, canteen_id=57)
Canteen('je-zeiss', parser, canteen_id=58)
Canteen('je-eah', parser, canteen_id=61)
Canteen('je-ernstabbe', parser, canteen_id=41)
Canteen('je-vegeTable', parser, canteen_id=60)
Canteen('je-rosen', parser, canteen_id=63)
Canteen('je-philosophen', parser, canteen_id=59)
Canteen('je-haupt', parser, canteen_id=64)
Canteen('je-bib', parser, canteen_id=65)
Canteen('nh-mensa', parser, canteen_id=71)
Canteen('sk-mensa', parser, canteen_id=73)
Canteen('we-park', parser, canteen_id=77)
Canteen('we-anna', parser, canteen_id=80)
Canteen('we-coudray', parser, canteen_id=81)
