from magdeburg import parse_url as magdeburg_parse
from hannover import parse_url as hannover_parse
from karlsruhe import parse_url as karlsruhe_parse
from leipzig import parse_url as leipzig_parse

providers = {
	'magdeburg': {
		'handler': magdeburg_parse,
		'prefix': 'http://www.studentenwerk-magdeburg.de/mensen-cafeterien/',
		'canteens': {
			'ovgu-unten': 'mensa-unicampus/speiseplan-unten/',
			'ovgu-oben': 'mensa-unicampus/speiseplan-oben/',
			'herrenkrug': 'mensa-herrenkrug/speiseplan/',
			'stendal': 'mensa-stendal/speiseplan/',
			'halberstadt': 'mensa-halberstadt/speiseplan/',
			'wernigerode': 'mensa-wernigerode/speiseplan/'
		}
	},
	'hannover': {
		'handler': hannover_parse,
		'prefix': 'http://www.stwh-portal.de/mensa/index.php?format=txt&wo=',
		'canteens': {
			'hauptmensa': '2',
			'hauptmensa-marktstand': '9',
			'restaurant-ct': '10',
			'contine': '3',
			'pzh': '13',
			'caballus': '1',
			'tiho-tower': '0',
			'hmtmh': '8',
			'ricklinger-stadtweg': '6',
			'kurt-schwitters-forum': '7',
			'blumhardtstrasse': '14',
			'herrenhausen': '12',
		}
	},
	'karlsruhe': {
		'handler': karlsruhe_parse,
		'prefix': 'http://www.studentenwerk-karlsruhe.de/de/essen/',
		'canteens': {
			'adenauerring': ('', ('canteen_place_1',)),
			'moltke': ('', ('canteen_place_2',)),
			'erzbergerstrasse': ('', ('canteen_place_3',)),
			'schloss-gottesaue': ('', ('canteen_place_4',)),
			'tiefenbronner-strasse': ('', ('canteen_place_5',)),
			'holzgartenstrasse': ('', ('canteen_place_6',))
		}
	},
	'leipzig': {
		'handler': leipzig_parse,
		'prefix': 'http://www.studentenwerk-leipzig.de/mensen-und-cafeterien/speiseplan/m/meals.php?canteen=',
		'canteens': {
			'dittrichring': '153',
			'koburger-straße': '121',
			'philipp-rosenthal-strasse': '127',
			'waechterstrasse': '129',
			'academica': '118',
			'am-park': '106',
			'am-elsterbecken': '115',
			'liebigstrasse': '162',
			'peterssteinweg': '111',
			'schoenauer-strasse': '140',
			'tierklinik': '170'
		}
	}
}


def parse(provider, canteen):
	if provider not in providers:
		return False
	provider = providers[provider]
	if canteen not in provider['canteens']:
		return False
	canteen = provider['canteens'][canteen]
	if type(canteen) is tuple:
		return provider['handler'](provider['prefix'] + canteen[0], *canteen[1])
	else:
		return provider['handler'](provider['prefix'] + canteen)
