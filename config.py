from magdeburg import parse_url as magdeburg_parse
from hannover import parse_url as hannover_parse

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
