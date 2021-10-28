import re
import os.path as path
from urllib.request import urlopen

from bs4 import BeautifulSoup as parse

from utils import Parser
from pyopenmensa.feed import LazyBuilder, extractNotes

price_regex = re.compile(r'(?P<price>\d+[,.]\d{2}) ?€')
legend_regex = re.compile(r'(?P<name>(\w{1,3}))\s=\s(?P<value>\w+((\s+\w+)*))$')

canteens = {
  # API Extraction: https://github.com/kreativmonkey/jgu-mainz-openmensa/issues/1
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

extraLegend = {
  # Source: https://www.studierendenwerk-mainz.de/essen-trinken/speiseplan
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
  }

iconLegend = {
  # Removed parts are in the extrasLegend!
  #'S.png' : 'Scheinefleisch',
  #'R.png' : 'Rindfleisch',
  'Fi.png' : 'Fisch',
  'Lamm.png' : 'Enthält Lammfleisch',
  'W.png' : 'Wildgericht',
  'Gl.png' : 'Glutenfrei',
  'La.png' : 'Lactosefrei',
  'Vegan.png' : 'Vegan',
  'Veggi.png' : 'Vegetarisch',
  'mensa-vital-small-2.png' : 'Mensa Vital'
  }

def get_icon_notes(meal):
  images = meal.find_all('img')
  notes = []
      
  # Extracting the icons with special informations about the meal
  # Example: <img src="/fileadmin/templates/images/speiseplan/Veggi.png"/>
  for icon in images:
    icon_name = path.basename(icon['src'])
    if icon_name in iconLegend:
      notes.append(iconLegend[icon_name])

  return notes

def build_meal_price(meal):
  meal_prices = {}

  prices = price_regex.findall(str(meal))
  # The pricing for employee and others are the same!
  meal_prices["student"] = prices[0].replace(',', '.')
  meal_prices["employee"] = prices[1].replace(',', '.')
  meal_prices["other"] = prices[1].replace(',', '.')

  return meal_prices
    
def parse_data(canteen, data):
  date = None
  category = None

  # We assume that the `div`s appear in a certain order and will associate each meal to the previously encountered date and category.
  for v in data.find_all('div'):
    if not v.has_attr('class'):
      continue

    if 'speiseplan_date' in v['class']:
      date = str(v.string).strip()
      
    if 'speiseplancounter' in v['class']:
      # Save the countername as category to list meals by counter
      category = str(v.string).strip()
      
    if 'menuspeise' in v['class']:
      meal_name = str(v.find('div', class_="speiseplanname").string).strip()
      meal_notes = get_icon_notes(v)
      meal_prices = build_meal_price(v)

      if date and category:
        canteen.addMeal(date, category,
                meal_name, meal_notes, meal_prices)
 
def parse_url(url, today):
  canteen = LazyBuilder()
  canteen.setLegendData(extraLegend)

  # For today display:
  if today:
    with urlopen(url + '&display_type=1') as resp:
        resp = parse(resp.read().decode('utf-8', errors='ignore'), features='lxml')
        speiseplan = resp.find('div', class_='speiseplan')
      
    parse_data(canteen, speiseplan)
  # For week display:
  else:
    for d in display:
      with urlopen(url + '&display_type=' + d) as resp:
        resp = parse(resp.read().decode('utf-8', errors='ignore'), features='lxml')
        speiseplan = resp.find('div', class_='speiseplan')
    
      parse_data(canteen, speiseplan)
    
  return canteen.toXMLFeed()

# The shared_prefix is the page where the Website it self gets its data from.
parser = Parser('mainz',
      handler=parse_url,
      shared_prefix='https://www.studierendenwerk-mainz.de/essen-trinken/speiseplan')

for canteen in canteens:
  parser.define(canteens[canteen], suffix='?building_id='+canteen) 
