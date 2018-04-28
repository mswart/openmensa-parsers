from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from utils import Parser
from datetime import datetime, timedelta
from pyopenmensa.feed import LazyBuilder

calendar_week_regex = re.compile('\d{4}-\d{1,2}$')
week_start_end_date_regex = re.compile('\d{1,2}\.\d{1,2}\.\d{4}')
fees_regex = re.compile('Bedienstete.*')
amount_regex = re.compile('\d{1,2},\d{1,2}')
days_regex = re.compile('day_\d$')
ingredients_regex = re.compile('Inhalt:.*')


def parse_url(url, today=False):
	canteen = LazyBuilder()
	content = urlopen(url).read()
	document = parse(content, 'lxml')
	employees_fee = 1.8
	guests_fee = 3.2
	fees = document.find_all('p', {'class': 'MsoNormal'})
	for fee_candidate in fees:
		fee_string = fees_regex.findall(fee_candidate.text)
		for s in fee_string:
			amount_strings = amount_regex.findall(s)
			if len(amount_strings) is not 2:
				continue
			employees_fee = float(amount_strings[0].replace(',', '.'))
			guests_fee = float(amount_strings[1].replace(',', '.'))
	options = document.find_all('option', value=calendar_week_regex)
	for option in options:
		try:
			_ = option['selected']
			start_end_dates = week_start_end_date_regex.findall(option.text)
			start_date_str = start_end_dates[0]
			mensa_start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
			days = document.find_all('div', id=days_regex)
			days_open = []
			for day in days:
				day_id = int(day['id'][-1:])
				days_open.append(day_id)
				current_date = mensa_start_date + timedelta(days=day_id-2)
				meals_data = day.find_all('tr')
				for meal_data in meals_data:
					meals = meal_data.find_all('td')
					if len(meals) is not 3:
						continue
					notes = [meals[0].text]
					ingredients = ingredients_regex.findall(meals[1].text)
					if len(ingredients) > 0:
						notes.append(ingredients[0].strip())
					main_dish = ingredients_regex.sub('', meals[1].text).strip()
					students_fee_string = amount_regex.findall(meals[2].text)
					if len(students_fee_string) is not 1:
						continue
					students_fee = float(students_fee_string[0].replace(',', '.'))
					costs = {'student': students_fee,
							 'employee': students_fee + employees_fee,
							 'other': students_fee + guests_fee}
					canteen.addMeal(current_date.date(), 'Hauptgerichte', main_dish, notes, costs,
									None)
				if today:
					return canteen.toXMLFeed()
			for i in range(2, 9):
				if i not in days_open:
					closed_date = mensa_start_date + timedelta(days=i-2)
					canteen.setDayClosed(closed_date.date())
		except Exception:
			continue

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


