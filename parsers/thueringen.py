from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from utils import EasySource, Parser, Source
from datetime import datetime, timedelta, date
from pyopenmensa.feed import LazyBuilder

amount_regex = re.compile('\d{1,2},\d{1,2}')


def find_start_date(document):
	calendar_week_regex = re.compile('\d{4}-\d{1,2}$')

	return document.find('option', value=calendar_week_regex, selected=True)


def parse_start_date(document):
	week_start_end_date_regex = re.compile('\d{1,2}\.\d{1,2}\.\d{4}')

	option = find_start_date(document)
	start_date_str = week_start_end_date_regex.search(option.text)

	return datetime.strptime(start_date_str.group(), '%d.%m.%Y').date()


def parse_available_weeks(document):
	sel_week = document.find('select', {"name": 'selWeek'})

	options = sel_week.find_all('option')

	for option in options:
		week = option['value']
		if week != '0':
			yield week


def parse_fees(document):
	fees_regex = re.compile('Bedienstete.*')

	fees = document.find_all('p', class_='MsoNormal', string=fees_regex)

	for fee in fees:
		fee_strings = fees_regex.findall(fee.text)
		for amount_candidate in fee_strings:
			amount_strings = amount_regex.findall(amount_candidate)
			if len(amount_strings) != 2:
				continue

			employees_fee = float(amount_strings[0].replace(',', '.'))
			guests_fee = float(amount_strings[1].replace(',', '.'))
			return employees_fee, guests_fee

	return None, None


def parse_ingredients(document):
	groups_regex = re.compile('([\w\d*]+):\s+(.*)')
	groups = dict()

	for table in document.select('div.kontextbox > table:nth-of-type(1)'):
		for s in table.stripped_strings:
			g = groups_regex.search(s)
			if g is not None:
				groups[g.group(1)] = g.group(2).strip()

	return groups


def parse_meals(day, groups):
	ingredients_regex = re.compile('Inhalt:.*')

	meals_t_rows = day.find_all('tr')

	for meal_data in meals_t_rows:
		meal_t_datas = meal_data.find_all('td')
		if len(meal_t_datas) != 3:
			continue

		category = meal_t_datas[0].text
		notes = []
		ingredients = ingredients_regex.findall(meal_t_datas[1].text)

		if len(ingredients) > 0:
			ingredients_list = ingredients[0][8:].strip().split(',')

			notes = [groups[note] for note in ingredients_list if note in groups]

		main_dish = ingredients_regex.sub('', meal_t_datas[1].text).strip()

		students_fee_string = amount_regex.findall(meal_t_datas[2].text)
		if len(students_fee_string) != 1:
			continue

		students_fee = float(students_fee_string[0].replace(',', '.'))
		costs = {'student': students_fee}

		# Skip empty meals
		if len(main_dish) == 0:
			continue

		yield (main_dish, notes, costs, category)


def parse_meals_for_canteen(document, canteen, employees_fee, guests_fee, groups, today):
	days_regex = re.compile('day_\d$')
	mensa_start_date = parse_start_date(document)

	day_divs = document.find_all('div', id=days_regex)

	for day in day_divs:
		day_id = int(day['id'][-1:])

		current_date = mensa_start_date + timedelta(days=day_id - 2)

		meals = parse_meals(day, groups)
		for meal in meals:
			main_dish, notes, costs, category = meal

			if employees_fee is not None:
				costs['employee'] = costs['student'] + employees_fee
			if guests_fee is not None:
				costs['other'] = costs['student'] + guests_fee
			if today and current_date != date.today():
				continue

			canteen.addMeal(current_date, category, main_dish, notes, costs,
							None)

class Canteen(EasySource):
	BASE_URL = 'http://www.stw-thueringen.de/deutsch/mensen/einrichtungen/'

	def __init__(self, *args, suffix):
		super().__init__(*args)
		self.suffix = suffix

	def parse_url(self, url, today=False):
		document = self.parse_remote(url)

		employees_fee, guests_fee = parse_fees(document)
		groups = parse_ingredients(document)

		# for the case that the start date is not auto set by the page e.g. on weekends
		noskip = find_start_date(document) is None
		available_weeks = parse_available_weeks(document)

		for idx, week in enumerate(available_weeks):
			if idx > 0 or noskip:
				document = self.parse_remote("{}?selWeek={}".format(url, week))

			parse_meals_for_canteen(document, self.feed, employees_fee, guests_fee, groups, today)
			if today:
				break

	def extract_metadata(self):
		city = self.suffix.split('/')[0]
		doc = self.parse_remote(self.BASE_URL + city)
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
		self.parse_url(self.BASE_URL + self.suffix, True)
		return self.feed.toXMLFeed()

	@Source.full_feed
	def full(self, request):
		self.parse_url(self.BASE_URL + self.suffix, False)
		return self.feed.toXMLFeed()

parser = Parser('thueringen', version='1.0')
Canteen('ei-wartenberg', parser, suffix='eisenach/mensa-am-wartenberg-2.html')
Canteen('ef-nordhaeuser', parser, suffix='erfurt/mensa-nordhaeuser-strasse.html')
Canteen('ef-altonaer', parser, suffix='erfurt/mensa-altonaer-strasse.html')
Canteen('ef-schlueterstr', parser, suffix='erfurt/cafeteria-schlueterstrasse.html')
Canteen('ef-leipzigerstr', parser, suffix='erfurt/cafeteria-leipziger-strasse.html')
Canteen('ge-freundschaft', parser, suffix='gera/mensa-weg-der-freundschaft.html')
Canteen('il-ehrenberg', parser, suffix='ilmenau/mensa-ehrenberg.html')
Canteen('il-cafeteria', parser, suffix='ilmenau/cafeteria-mensa-ehrenberg.html')
Canteen('il-nanoteria', parser, suffix='ilmenau/cafeteria-nanoteria.html')
Canteen('il-roentgen', parser, suffix='ilmenau/cafeteria-roentgenbau.html')
Canteen('je-zeiss', parser, suffix='jena/mensa-carl-zeiss-promenade.html')
Canteen('je-eah', parser, suffix='jena/cafeteria-eah.html')
Canteen('je-ernstabbe', parser, suffix='jena/mensa-ernst-abbe-platz.html')
Canteen('je-vegeTable', parser, suffix='jena/vegetable.html')
Canteen('je-rosen', parser, suffix='jena/cafeteria-zur-rosen.html')
Canteen('je-philosophen', parser, suffix='jena/mensa-philosophenweg.html')
Canteen('je-haupt', parser, suffix='jena/cafeteria-uni-hauptgebaeude.html')
Canteen('je-bib', parser, suffix='jena/cafeteria-bibliothek-thulb.html')
Canteen('nh-mensa', parser, suffix='nordhausen/mensa-nordhausen.html')
Canteen('sk-mensa', parser, suffix='schmalkalden/mensa-schmalkalden.html')
Canteen('we-horn', parser, suffix='weimar/cafeteria-am-horn.html')
Canteen('we-park', parser, suffix='weimar/mensa-am-park.html')
Canteen('we-anna', parser, suffix='weimar/cafeteria-anna-amalia-bibliothek.html')
Canteen('we-coudray', parser, suffix='weimar/cafeteria-coudraystrasse.html')
