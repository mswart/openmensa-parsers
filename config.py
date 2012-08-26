from magdeburg import parse_url as magdeburg_parse
from hannover import parse_url as hannover_parse
from karlsruhe import parse_url as karlsruhe_parse
from leipzig import parse_url as leipzig_parse
from dresden import parse_url as dresden_parse
from aachen import parse_url as aachen_parse
from wuerzburg import parse_url as wuerzburg_parse
from marburg import parse_url as marburg_parse
from hamburg import parse_url as hamburg_parse
from muenchen import parse_url as muenchen_parse

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
			'adenauerring': ('', 'canteen_place_1'),
			'moltke': ('', 'canteen_place_2'),
			'erzbergerstrasse': ('', 'canteen_place_3'),
			'schloss-gottesaue': ('', 'canteen_place_4'),
			'tiefenbronner-strasse': ('', 'canteen_place_5'),
			'holzgartenstrasse': ('', 'canteen_place_6')
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
	},
	'dresden': {
		'handler': dresden_parse,
		'prefix': 'http://www.studentenwerk-dresden.de/mensen/speiseplan/',
		'canteens': {
			'neue-mensa': 'neue-mensa',
			'alte-mensa': 'alte-mensa',
			'reichenbachstrasse': 'mensa-reichenbachstrasse',
			'mensologie': 'mensologie',
			'siedepunkt': 'mensa-siedepunkt',
			'tellerrandt': 'mensa-tellerrandt',
			'palucca-schule': 'mensa-palucca-schule',
			'blau': 'mensa-blau',
			'stimm-gabel': 'mensa-stimm-gabel',
			'johannstadt': 'mensa-johannstadt',
			'u-boot': 'u-boot',
			'zittau': 'mensa-zittau',
			'haus-vii': 'mensa-haus-vii',
			'goerlitz': 'mensa-goerlitz',
			'sport': 'mensa-sport',
			'kreuzgymnasium': 'mensa-kreuzgymnasium',
		}
	},
	'aachen': {
		'handler': aachen_parse,
		'prefix': 'http://speiseplan.studentenwerk-aachen.de/mensa/',
		'canteens': {
			'zeltmensa': 'wo_mensa1_turm.std.php',
			'templergraben': 'wo_bistro_templer.std.php',
			'ahorn': 'wo_mensa_ahorn.std.php',
			'vita': 'wo_mensa_vita.std.php',
			'bayernallee': 'wo_mensa3_bayern.std.php',
			'eups': 'wo_mensa_eups.std.php',
			'goethe': 'wo_gastro_goethe.std.php',
			'juelich': 'wo_mensa4_juelich.std.php'
		},
	},
	'wuerzburg': {
		'handler': wuerzburg_parse,
		'prefix': 'http://www.studentenwerk-wuerzburg.de/essen-trinken/speiseplaene/plan/show/',
		'canteens': {
			'austrasse': 'austrasse-bamberg.html',
			'burse': 'burse-wuerzburg.html',
			'feldkirchenstrasse': 'feldkirchenstrasse-bamberg.html',
			'frankenstube': 'frankenstube-wuerzburg.html',
			'hubland': 'mensa-am-hubland-wuerzburg.html',
			'studentenhaus': 'mensa-am-studentenhaus.html',
			'aschaffenburg': 'mensa-aschaffenburg',
			'augenklinik': 'mensa-augenklinik-wuerzburg.html',
			'josef-schneider': 'mensa-josef-schneider-strasse-wuerzburg.html',
			'schweinfurt': 'mensa-schweinfurt.html',
		},
	},
	'marburg': {
		'handler': marburg_parse,
		'prefix': 'http://www.studentenwerk-marburg.de/essen-trinken/speiseplan/',
		'canteens': {
			'bistro': ('', 'Speiseplan.*Bistro', 'diese-woche-bistro.html', 'naechste-woche-bistro.html'),
			'mos-diner': ('', 'Speiseplan.*Diner', 'diese-woche-mos-diner.html'),
			'erlenring': ('', 'Mensa Erlenring', 'diese-woche-mensa-erlenring-und-lahnberge.html',
					'naechste-woche-mensa-erlenring-und-lahnberge.html' ),
			'lahnberge': ('', 'Mensa Lahnberge', 'diese-woche-mensa-erlenring-und-lahnberge.html',
					'naechste-woche-mensa-erlenring-und-lahnberge.html' ),
		}
	},
	'hamburg': {
		'handler': hamburg_parse,
		'prefix': 'http://speiseplan.studwerk.uptrade.de/index.php/de/',
		'canteens': {
			'armgartstrasse':        '590',
			'bergedorf':            '520',
			'berliner-tor':         '530',
			'averhoffstrasse':       '650',
			'botanischer-garten':   '560',
			'bucerius-law-school':  '410',
			'cafe-jungiusstrasse':   '610',
			'cafe-alexanderstrasse': '660',
			'campus':               '340',
			'city-nord':            '550',
			'finkenau':             '620',
			'geomatikum':           '540',
			'harburg':              '570',
			'philosophenturm':      '350',
			'stellingen':           '580',
			'studierendenhaus':     '310',
		}
	},
	'muenchen': {
		'handler': muenchen_parse,
		'prefix': 'http://www.studentenwerk-muenchen.de/mensa/speiseplan/',
		'canteens': {
			'leopoldstrasse':      'speiseplan_{}_411_-de.html',
			'martinsried':         'speiseplan_{}_412_-de.html',
			'grosshadern':         'speiseplan_{}_414_-de.html',
			'schellingstrasse':    'speiseplan_{}_416_-de.html',
			'goethestrasse':       'speiseplan_{}_418_-de.html',
			'archisstrasse':       'speiseplan_{}_421_-de.html',
			'garching':            'speiseplan_{}_422_-de.html',
			'weihenstephan':       'speiseplan_{}_423_-de.html',
			'lothstrasse':         'speiseplan_{}_431_-de.html',
			'pasing':              'speiseplan_{}_432_-de.html',
			'olympiapark':         'speiseplan_{}_523_-de.html',
			'cafeteria-garching':  'speiseplan_{}_524_-de.html',
			'akademie':            'speiseplan_{}_526_-de.html',
			'boltzmannstrasse':    'speiseplan_{}_527_-de.html',
		}
	},
}


def parse(provider, canteen):
	if provider not in providers:
		return False
	provider = providers[provider]
	if canteen not in provider['canteens']:
		return False
	canteen = provider['canteens'][canteen]
	if type(canteen) is tuple:
		return provider['handler'](provider['prefix'] + canteen[0], *canteen[1:])
	else:
		return provider['handler'](provider['prefix'] + canteen)
