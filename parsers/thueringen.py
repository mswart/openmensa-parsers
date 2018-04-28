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
	options = document.find_all('option', value=calendar_week_regex)
	assert len(options) > 0
	options_filtered = list(filter(lambda x: x.has_attr('selected'), options))
	assert len(options_filtered) is 1
	option = options_filtered[0]
	start_date_strings = week_start_end_date_regex.findall(option.text)
	assert len(start_date_strings) > 0
	start_date_str = start_date_strings[0]
	return datetime.strptime(start_date_str, '%d.%m.%Y')


def parse_fees(document):
	fees_regex = re.compile('Bedienstete.*')
	fees_p = document.find_all('p', {'class': 'MsoNormal'})
	for fee_candidate in fees_p:
		fee_strings = fees_regex.findall(fee_candidate.text)
		for amount_candidate in fee_strings:
			amount_strings = amount_regex.findall(amount_candidate)
			if len(amount_strings) is not 2:
				continue
			employees_fee = float(amount_strings[0].replace(',', '.'))
			guests_fee = float(amount_strings[1].replace(',', '.'))
			return employees_fee, guests_fee
	return -1, -1


def parse_meals(day):
	ingredients_regex = re.compile('Inhalt:.*')
	meals = []
	meals_t_rows = day.find_all('tr')
	for meal_data in meals_t_rows:
		meal_t_datas = meal_data.find_all('td')
		if len(meal_t_datas) is not 3:
			continue
		notes = [meal_t_datas[0].text]
		ingredients = ingredients_regex.findall(meal_t_datas[1].text)
		if len(ingredients) > 0:
			notes.append(ingredients[0].strip())
		main_dish = ingredients_regex.sub('', meal_t_datas[1].text).strip()
		students_fee_string = amount_regex.findall(meal_t_datas[2].text)
		if len(students_fee_string) is not 1:
			continue
		students_fee = float(students_fee_string[0].replace(',', '.'))
		costs = {'student': students_fee}
		meals.append((main_dish, notes, costs))
	return meals


def parse_url(url, today=False):
	days_regex = re.compile('day_\d$')
	employees_fee = 1.8
	guests_fee = 3.2
	canteen = LazyBuilder()
	content = urlopen(url).read()
	document = parse(content, 'lxml')
	fees = parse_fees(document)
	if len(fees) is 2:
		employees_fee = fees[0]
		guests_fee = fees[1]
	try:
		mensa_start_date = parse_start_date(document)
	except AssertionError:
		return canteen.toXMLFeed()
	day_divs = document.find_all('div', id=days_regex)
	days_open = []
	for day in day_divs:
		day_id = int(day['id'][-1:])
		days_open.append(day_id)
		current_date = mensa_start_date + timedelta(days=day_id-2)
		meals = parse_meals(day)
		for meal in meals:
			main_dish = meal[0]
			notes = meal[1]
			costs = meal[2]
			if employees_fee is not -1:
				costs['employee'] = costs['student'] + employees_fee
			if guests_fee is not -1:
				costs['other'] = costs['student'] + guests_fee
			if today:
				if current_date.day is datetime.today().day:
					canteen.addMeal(current_date.date(), 'Hauptgerichte', main_dish, notes, costs,
									None)
			else:
				canteen.addMeal(current_date.date(), 'Hauptgerichte', main_dish, notes, costs,
								None)
	for i in range(min(days_open), 9):
		if i not in days_open:
			closed_date = mensa_start_date + timedelta(days=i-2)
			if not today or closed_date.day is datetime.today().day:
				canteen.setDayClosed(closed_date.date())

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
parser.define('ilroentgen', suffix='ilmenau/cafeteria-roentgenbau.html')
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
