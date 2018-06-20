from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from utils import Parser
from datetime import datetime, timedelta
from pyopenmensa.feed import LazyBuilder

amount_regex = re.compile('\d{1,2},\d{1,2}')


def parse_start_date(document):
	week_start_end_date_regex = re.compile('\d{1,2}\.\d{1,2}\.\d{4}')
	calendar_week_regex = re.compile('\d{4}-\d{1,2}$')

	option = document.find("option", value=calendar_week_regex, selected=True)

	if option is None:
		return None

	start_date_str = week_start_end_date_regex.search(option.text)

	return datetime.strptime(start_date_str.group(), '%d.%m.%Y')


def parse_fees(document):
	fees_regex = re.compile('Bedienstete.*')

	fees = document.find_all('p', class_='MsoNormal', string=fees_regex)

	if len(fees) != 1:
		return None, None

	fees = fees[0]

	fee_strings = fees_regex.findall(fees.text)
	for amount_candidate in fee_strings:
		amount_strings = amount_regex.findall(amount_candidate)
		if len(amount_strings) != 2:
			continue

		employees_fee = float(amount_strings[0].replace(',', '.'))
		guests_fee = float(amount_strings[1].replace(',', '.'))
		return employees_fee, guests_fee

	return None, None


def parse_ingredients(document):
	contextbox = document.find('div', class_='kontextbox')

	shorts = contextbox.find_all('p')

	digits_regex = re.compile('(\d)+: .*')
	chars_regex = re.compile('(\w)+: .*')

	digits = dict()
	chars = dict()

	if len(shorts) < 3:
		return
	for short in shorts[1].childGenerator():
		if digits_regex.search(str(short)):
			n = str(short).strip('\r\n').split(':')
			digits[n[0]] = n[1]

	for short in shorts[2].childGenerator():
		if chars_regex.search(str(short)):
			c = str(short).strip('\r\n').split(':')
			chars[c[0]] = c[1]

	shorts = contextbox.find_all('td')

	if len(shorts) >= 1:
		for short in shorts[1].childGenerator():
			if chars_regex.search(str(short)):
				c = str(short).strip('\r\n').split(':')
				chars[c[0]] = c[1]

	return digits, chars


def ingredient_list_to_notes(ingredients_list, chars, digits):
	ingredients = []
	for ingredient in ingredients_list:

		if digits.get(ingredient) is not None:
			ingredients.append(digits[ingredient][1:])

		if chars.get(ingredient) is not None:
			ingredients.append(chars[ingredient][1:])

	return ingredients


def parse_meals(day, digits, chars):
	ingredients_regex = re.compile('Inhalt:.*')

	meals_t_rows = day.find_all('tr')

	for meal_data in meals_t_rows:
		meal_t_datas = meal_data.find_all('td')
		if len(meal_t_datas) != 3:
			continue

		category = [meal_t_datas[0].text]
		if len(category) == 1:
			category = category[0]
		else:
			category = 'Hauptgerichte'

		notes = []
		ingredients = ingredients_regex.findall(meal_t_datas[1].text)

		if len(ingredients) > 0:
			ingredients_list = ingredients[0].strip('Inhalt: ').strip('\r').split(',')

			notes = ingredient_list_to_notes(ingredients_list, chars, digits)

		main_dish = ingredients_regex.sub('', meal_t_datas[1].text).strip()

		students_fee_string = amount_regex.findall(meal_t_datas[2].text)
		if len(students_fee_string) != 1:
			continue

		students_fee = float(students_fee_string[0].replace(',', '.'))
		costs = {'student': students_fee}

		yield (main_dish, notes, costs, category)


def parse_url(url, today=False):
	year = datetime.now().isocalendar()[0]
	week = datetime.now().isocalendar()[1]

	days_regex = re.compile('day_\d$')

	canteen = LazyBuilder()

	for i in range(0, 3):

		content = urlopen(url+'?selWeek='+str(year)+'-'+str(week + i)).read()

		document = parse(content, 'lxml')

		employees_fee, guests_fee = parse_fees(document)

		mensa_start_date = parse_start_date(document)

		day_divs = document.find_all('div', id=days_regex)

		for day in day_divs:
			day_id = int(day['id'][-1:])

			current_date = mensa_start_date + timedelta(days=day_id-2)
			digits, chars = parse_ingredients(document)
			meals = parse_meals(day, digits, chars)
			for meal in meals:
				main_dish, notes, costs, category = meal

				if employees_fee is not None:
					costs['employee'] = costs['student'] + employees_fee
				if guests_fee is not None:
					costs['other'] = costs['student'] + guests_fee
				if today and current_date != datetime.today():
					continue

				canteen.addMeal(current_date.date(), category, main_dish, notes, costs,
									None)

	return canteen.toXMLFeed()


parser = Parser('thueringen',
				handler=parse_url,
				shared_prefix='http://www.stw-thueringen.de/deutsch/mensen/einrichtungen/')
parser.define('ei-wartenberg', suffix='eisenach/mensa-am-wartenberg-2.html')
parser.define('ef-nordhaeuser', suffix='erfurt/mensa-nordhaeuser-strasse.html')
parser.define('ef-altonaer', suffix='erfurt/mensa-altonaer-strasse.html')
parser.define('ef-schlueterstr', suffix='erfurt/cafeteria-schlueterstrasse.html')
parser.define('ef-leipzigerstr', suffix='erfurt/cafeteria-leipziger-strasse.html')
parser.define('ge-freundschaft', suffix='gera/mensa-weg-der-freundschaft.html')
parser.define('il-ehrenberg', suffix='ilmenau/mensa-ehrenberg.html')
parser.define('il-cafeteria', suffix='ilmenau/cafeteria-mensa-ehrenberg.html')
parser.define('il-nanoteria', suffix='ilmenau/cafeteria-nanoteria.html')
parser.define('il-roentgen', suffix='ilmenau/cafeteria-roentgenbau.html')
parser.define('je-zeiss', suffix='jena/mensa-carl-zeiss-promenade.html')
parser.define('je-eah', suffix='jena/cafeteria-eah.html')
parser.define('je-ernstabbe', suffix='jena/mensa-ernst-abbe-platz.html')
parser.define('je-vegeTable', suffix='jena/vegetable.html')
parser.define('je-rosen', suffix='jena/cafeteria-zur-rosen.html')
parser.define('je-philosophen', suffix='jena/mensa-philosophenweg.html')
parser.define('je-haupt', suffix='jena/cafeteria-uni-hauptgebaeude.html')
parser.define('je-bib', suffix='jena/cafeteria-bibliothek-thulb.html')
parser.define('nh-mensa', suffix='nordhausen/mensa-nordhausen.html')
parser.define('sk-mensa', suffix='schmalkalden/mensa-schmalkalden.html')
parser.define('we-horn', suffix='weimar/cafeteria-am-horn.html')
parser.define('we-park', suffix='weimar/mensa-am-park.html')
parser.define('we-anna', suffix='weimar/cafeteria-anna-amalia-bibliothek.html')
parser.define('we-coudray', suffix='weimar/cafeteria-coudraystrasse.html')
