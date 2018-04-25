from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
from utils import Parser
from datetime import datetime, timedelta
from pyopenmensa.feed import LazyBuilder

calendar_week_regex = re.compile('\d{4}-\d{1,2}$')
week_start_end_date_regex = re.compile('\d{1,2}.\d{1,2}.\d{4}')
days_regex = re.compile('day_\d$')
ingredients_regex = re.compile('Inhalt:.*')


def parse_url(url, today=False):
	canteen = LazyBuilder()
	content = urlopen(url).read()
	document = parse(content, 'lxml')
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
					canteen.addMeal(current_date.date(), 'Hauptgerichte', main_dish, notes, {'student': meals[2].text},
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


parser = Parser('ilmenau',
				handler=parse_url,
				shared_prefix='http://www.stw-thueringen.de/deutsch/mensen/einrichtungen/ilmenau/')
parser.define('ehrenberg', suffix='mensa-ehrenberg.html')
parser.define('cafeteria', suffix='cafeteria-mensa-ehrenberg.html')
parser.define('nanoteria', suffix='cafeteria-nanoteria.html')
parser.define('roentgen', suffix='cafeteria-roentgenbau.html')
