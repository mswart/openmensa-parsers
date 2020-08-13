from urllib.request import urlopen
from bs4 import BeautifulSoup as parse
import re
import datetime
import os.path as path

from utils import Parser
from pyopenmensa.feed import OpenMensaCanteen


day_regex = re.compile('(?P<date>\d{4}-\d{2}-\d{2})')
price_regex = re.compile('(?P<price>\d+[,.]\d{2}) ?€')
notes_regex = re.compile('\[(?:(([A-Za-z0-9]+),?)+)\]$')
extract_legend = re.compile('\((\w+,?)+\)')
extract_legend_notes = re.compile('(?:([A-Za-z0-9]+))')
extract_notes_regex = re.compile('(?:([A-Za-z0-9]+)[,|\)])')

canteenLegend = {
  # API Extraction: https://github.com/kreativmonkey/jgu-mainz-openmensa/issues/1
  '0' : 'all',
  '1' : 'zentralmensa',
  '2' : 'mensa-georg-foster',
  '3' : 'cafe-rewi',
  '4' : 'mensa-bingen',
  '5' : 'mensa-K3',
  '6' : 'mensa-holzstraße',
  '7' : 'mensarium',
  '8' : 'cafe-bingen-rochusberg',
  '9' : 'mensablitz'
}

display = {
  '2' : 'Aktuelle Woche',
  '3' : 'Nächste Woche'
}

roles = ('student', 'other', 'employee')

extraLegend = {
    # Source: https://www.studierendenwerk-mainz.de/essentrinken/speiseplan/
    '1': 'mit Farbstoff',
    '2': 'mit Konservierungsstoff',
    '3': 'mit Antioxidationsmittel',
    '4': 'mit Geschmacksverstärker',
    '5': 'geschwefelt',
    '6': 'geschwärzt',
    '7': 'gewachst',
    '8': 'Phosphat',
    '9': 'mit Süßungsmitteln',
    '10': 'enthält eine Phenylalaninquelle',
    'S' : 'Schweinefleisch',
    'G' : 'Geflügelfleisch',
    'R' : 'Rindfleisch',
    'Gl' : 'Gluten',
    'We' : 'Weizen (inkl. Dinkel)',
    'Ro' : 'Roggen',
    'Ge' : 'Gerste',
    'Haf': 'Hafer',
    'Kr' : 'Krebstiere und Krebstiererzeugnisse',
    'Ei' : 'Eier und Eiererzeugnisse',
    'Fi' : 'Fisch und Fischerzeugnisse',
    'En' : 'Erdnüsse und Erdnusserzeugnisse',
    'So' : 'Soja und Sojaerzeugnisse',
    'La' : 'Milch und Milcherzeugnisse',
    'Sl' : 'Sellerie und Sellerieerzeugnisse',
    'Sf' : 'Senf und Senferzeugnisse',
    'Se' : 'Sesamsamen und Sesamsamenerzeugnisse',
    'Sw' : 'Schwefeldioxid und Sulfite > 10mg/kg',
    'Lu' : 'Lupine und Lupinerzeugnisse',
    'Wt' : 'Weichtiere und Weichtiererzeugnisse',
    'Nu' : 'Schalenfrüchte',
    'Man': 'Mandel',
    'Has': 'Haselnüsse',
    'Wa' : 'Walnüsse',
    'Ka' : 'Kaschunüsse',
    'Pe' : 'Pecanüsse',
    'Pa' : 'Paranüsse',
    'Pi' : 'Pistatien',
    'Mac': 'Macadamianüsse',
    'icon:S.png' : 'Scheinefleisch',
    'icon:R.png' : 'Rindfleisch',
    'icon:Fi.png' : 'Fisch',
    'icon:Gl.png' : 'Glutenfrei',
    'icon:La.png' : 'Lactosefrei',
    'icon:Vegan.png' : 'Vegan',
    'icon:Veggi.png' : 'Vegetarisch'
    
}

def build_meal_name(meal):
	# Name des Gerichts
	name = str(meal).strip()
	# Remove the notes from Mealname and delete unnecessary spaces
	name = ' '.join(re.sub(r'\((\w+,?)+\)', '', name).split())
	if len(name) > 250:
			name = name[:245] + '...' 
	
	return name
	
def extract_meal_notes(meal):
	# extracting the legend
	legpart = extract_legend.findall(str(meal).strip())
	legend = []
	for l in legpart:
		legend.extend(extract_legend_notes.findall(l))
	
	notes = set()
	for l in legend:
		if extraLegend[l]:
			notes.add(extraLegend[l])
	
	return notes
	
def build_meal_notes(meal):
	notes = set()
			
	for icon in meal.find_all('img'):
		#<img src="/fileadmin/templates/images/speiseplan/Fi.png"/>
		#<img src="/fileadmin/templates/images/speiseplan/La.png"/>
		if "icon:"+path.basename(icon['src']) in extraLegend:
			notes.add(extraLegend["icon:"+path.basename(icon['src'])])
			
	# extracting the legend
	notes.update(extract_meal_notes(meal.find('div', class_="speiseplanname").string))
	
	return list(notes)
	
def build_meal_price(meal):
	# Preis aus v extrahieren
	# 3,40 € / 5,65 €
	meal_prices = {}
	
	prices = price_regex.findall(str(meal))
	# s = student
	# g = other
	# m = employee
	meal_prices["student"] = prices[0].replace(',', '.')
	meal_prices["employee"] = prices[1].replace(',', '.')
	meal_prices["other"] = prices[1].replace(',', '.')
	
	return meal_prices

def build_meal_date(meal):
	# Print the String of Date
	# Format: Montag, 12. August 2020
	# Output: 12. August 2020
	
	return meal
	
	
def parse_data(canteen, data):	
	for v in data.find_all('div'):
		if not v.has_attr('class'):
		  continue

		if v['class'][0] == 'speiseplan_date':
		  date = build_meal_date(str(v.string).strip())
				  
		if v['class'][0] == 'speiseplan_bldngall_name':
		  # Get Mensa Name
		  canteen_name = str(v.string).strip()
		  
		if v['class'][0] == 'speiseplancounter':
		  # Get Counter
		  counter_name = str(v.string).strip()
		  
		if v['class'][0] == 'menuspeise':
		  # Name des Gerichts
		  meal_name = build_meal_name(v.find('div', class_="speiseplanname").string)
		  meal_notes = build_meal_notes(v)
		  meal_prices = build_meal_price(v)

		  canteen.addMeal(date, counter_name,
							  meal_name, meal_notes, meal_prices)
	
	return canteen


def parse_url(url, today=False):
	#base_data = load_base_data()

	canteen = OpenMensaCanteen()
		
	for d in display:
		with urlopen(url + '&display_type=' + d) as resp:
			resp = parse(resp.read().decode('utf-8', errors='ignore'), features='lxml')
			speiseplan = resp.find('div', class_='speiseplan')
		
		canteen = parse_data(canteen, speiseplan)


	return canteen.toXMLFeed()

parser = Parser('mainz',
				handler=parse_url,
				shared_prefix='https://www.studierendenwerk-mainz.de/speiseplan/frontend/index.php')

for canteen in canteenLegend:
	parser.define(canteenLegend[canteen], suffix='?building_id='+canteen) 

