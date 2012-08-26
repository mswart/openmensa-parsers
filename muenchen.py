#!python3
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as parse
import re
import datetime

from helper import OpenMensaCanteen, extractWeekDates

price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€?')
otherPrice = re.compile('Gästezuschlag:? ?(?P<price>\d+[,.]\d{2}) ?€?')

def parse_url(url):
	canteen = OpenMensaCanteen()
	legend = {}
	document = parse(urlopen('http://www.studentenwerk-muenchen.de/mensa/speiseplan/zusatzstoffe-de.html').read())
	for td in document.find_all('td', class_='beschreibung'):
		legend[td.previous_sibling.previous_sibling.text] = td.text
	document = parse(urlopen('http://www.studentenwerk-muenchen.de/mensa/unsere-preise/').read())
	prices = {}
	for tr in document.find('table', class_='essenspreise').find_all('tr'):
		meal = tr.find('th')
		if not meal or not meal.text.strip(): continue
		if len(tr.find_all('td', class_='betrag')) < 3: continue
		meal = meal.text.strip()
		prices[meal] = {}
		for role, _id in [ ('student', 0), ('employee', 1), ('other', 2)]:
			prices[meal][role] = price_regex.search(
					tr.find_all('td', class_='betrag')[_id].text)\
					.group('price')
	errorCount = 0
	date = datetime.date.today()
	while errorCount < 7:
		try:
			document = parse(urlopen(url.format(date)).read())
		except HTTPError as e:
			if e.code == 404:
				errorCount += 1
				date += datetime.date.resolution
				continue
			else:
				raise e
		else:
			errorCount = 0
		for tr in document.find('table', class_='zusatzstoffe').find_all('tr'):
			legend[tr.find_all('td')[0].text.strip().replace('(', '').replace(')', '')] \
				= tr.find_all('td')[1].text.strip()
		canteen.setLegendData(legend)
		mensa_data = document.find('table', class_='menu')
		category = None
		for menu_tr in mensa_data.find_all('tr'):
			if menu_tr.find('td', class_='headline'):
				continue
			if menu_tr.find('td', class_='gericht').text:
				category = menu_tr.find('td', class_='gericht').text
			data = menu_tr.find('td', class_='beschreibung')
			name = data.find('span').text.strip()
			notes = [ span['title'] for span in data.find_all('span', title=True) ]
			canteen.addMeal(date, category, name, notes,
				prices.get(category.replace('Aktionsessen', 'Bio-/Aktionsgericht'), {}))
		date += datetime.date.resolution
	return canteen.toXMLFeed()
