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
extract_legend_notes = re.compile('(?<=[\(,])(\w{1,2})')

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

def build_meal_name(meal_name):
  # There are the extras of the meal inside the meal name
  # This will remove the extras and the unnecessary spaces
  # Example: 6 gebackene Fischstäbchen (Gl,Fi,We) mit Reis und veganem Joghurt-Kräuter-Dip (3,Gl,So,Sf,Ge)
  # Output: 6 gebackene Fischstäbchen mit Reis und veganem Joghurt-Kräuter-Dip
	name = ' '.join(re.sub(r'\((\w+,?)+\)', '', str(meal_name)).split())
  
  # Shorten the meal name to 250 characters
	if len(name) > 250:
			name = name[:245] + '...' 
	
	return name
	
def build_meal_notes(meal):
  meal_name = str(meal.find('div', class_="speiseplanname").string).strip()
  images = meal.find_all('img')

  # Use a set for easy elimination of duplicates
  notes = set()
      
  # extracting the icons with spezial informations about the meal
  # Example: <img src="/fileadmin/templates/images/speiseplan/Veggi.png"/>
  for icon in images:
    if "icon:"+path.basename(icon['src']) in extraLegend:
      notes.add(extraLegend["icon:"+path.basename(icon['src'])])

  for l in extract_legend_notes.findall(meal_name):
    if extraLegend[l]:
      notes.add(extraLegend[l])

  return list(notes)
	
def build_meal_price(meal):
	meal_prices = {}
	
	prices = price_regex.findall(str(meal))
  # The pricing for employee and others are the same!
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

