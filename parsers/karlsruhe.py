import datetime
import json
from urllib.request import urlopen

from utils import Parser

from pyopenmensa.feed import OpenMensaCanteen

CONST_META_URL = "https://www.sw-ka.de/en/json_interface/general/"
CONST_CANTEEN_URL = "https://www.sw-ka.de/en/json_interface/canteen/"

price_roles = [("price_1", "student"), ("price_2", "other"), ("price_3", "employee"), ("price_4", "pupil")]
def get_price_data(meal_data):
	prices = {}
	for role in price_roles:
		prices[role[1]] = meal_data[role[0]]
	return prices

pot_notes = [
	("bio", "kontrolliert biologischer Anbau mit EU Bio-Siegel / DE-Öko-007 Kontrollstelle"),
	("fish", "MSC aus zertifizierter Fischerei"),
	("pork", "enthält Schweinefleisch"),
	("pork_aw", "enthält regionales Schweinefleisch aus artgerechter Tierhaltung"),
	("cow", "enthält Rindfleisch"),
	("cow_aw", "enthält regionales Rindfleisch aus artgerechter Tierhaltung"),
	("vegan", "veganes Gericht"),
	("veg", "vegetarisches Gericht"),
	("mensa_vit", "Mensa Vital")
]
def get_notes(meal_data):
	notes = []
	if "info" in meal_data and (meal_data["info"] != None and meal_data["info"] != ""):
		notes.append(meal_data["info"])
	for pot_note in pot_notes:
		if meal_data[pot_note[0]]:
			notes.append(pot_note[1])
	return notes

def parse_url(url, place_class=None, today=False):
	canteen = OpenMensaCanteen()
	meta_data = json.load(urlopen(CONST_META_URL))
	canteen_data = json.load(urlopen(url))
	for day in canteen_data[place_class]:
		date = datetime.datetime.fromtimestamp(int(day))
		for line in canteen_data[place_class][day]:
			line_name = meta_data["mensa"][place_class]["lines"][line]
			for meal in canteen_data[place_class][day][line]:
				# why is meal not a key but the object?
				#meal_data = canteen_data[place_class][day][line][meal]
				meal_data = meal

				if "nodata" in meal_data and meal_data["nodata"]:
					continue;

				meal_name = meal_data["meal"]
				if "dish" in meal_data and (meal_data["dish"] != None and meal_data["dish"] != ""):
					meal_name += "\n"
					meal_name += meal_data["dish"]

				canteen.addMeal(date.strftime("%Y-%m-%d"), line_name, meal_name, get_notes(meal_data), get_price_data(meal_data))
	return canteen.toXMLFeed()


parser = Parser("karlsruhe", handler=parse_url, shared_args=[CONST_CANTEEN_URL])
parser.define("adenauerring", args=["adenauerring"])
parser.define("moltke", args=["moltke"])
parser.define("erzbergerstrasse", args=["erzbergerstrasse"])
parser.define("schloss-gottesaue", args=["gottesaue"])
parser.define("tiefenbronner-strasse", args=["tiefenbronner"])
parser.define("holzgartenstrasse", args=["holzgarten"])
parser.define("moltkestrasse", args=["x1moltkestrasse"])
