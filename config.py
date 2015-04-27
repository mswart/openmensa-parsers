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
from darmstadt import parse_url as darmstadt_parse
from niederbayern_oberpfalz import parse_url as niederbayern_oberpfalz_parse


providers = {
    'magdeburg': {
        'handler': magdeburg_parse,
        'prefix': 'http://www.studentenwerk-magdeburg.de/',
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
            'koburger-strasse': '121',
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
            'reichenbachstrasse': 'mensa-reichenbachstrasse',
            'zeltschloesschen': 'zeltschloesschen', # was neue mensa
            'alte-mensa': 'alte-mensa',
            'mensologie': 'mensologie',
            'siedepunkt': 'mensa-siedepunkt',
            'johannstadt': 'mensa-johannstadt',
            'wueins': 'mensa-wueins', # was blau
            'bruehl': 'mensa-bruehl',
            'u-boot': 'u-boot',
            'tellerrandt': 'mensa-tellerrandt',
            'zittau': 'mensa-zittau',
            'stimm-gabel': 'mensa-stimm-gabel',
            'palucca-schule': 'mensa-palucca-schule',
            'goerlitz': 'mensa-goerlitz',
            'sport': 'mensa-sport',
            'kreuzgymnasium': 'mensa-kreuzgymnasium',
        }
    },
    'aachen': {
        'handler': aachen_parse,
        'prefix': 'http://www.studentenwerk-aachen.de/speiseplaene/',
        'canteens': {
            'academica': 'academica-w.html',
            'ahorn': 'ahornstrasse-w.html',
            'templergraben': 'templergraben-w.html',
            'bayernallee': 'bayernallee-w.html',
            'eups': 'eupenerstrasse-w.html',
            'goethe': 'goethestrasse-w.html',
            'vita': 'vita-w.html',
            'zeltmensa': 'forum-w.html',
            'juelich': 'juelich-w.html',
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
                          'naechste-woche-mensa-erlenring-und-lahnberge.html'),
            'lahnberge': ('', 'Mensa Lahnberge', 'diese-woche-mensa-erlenring-und-lahnberge.html',
                          'naechste-woche-mensa-erlenring-und-lahnberge.html'),
        }
    },
    'hamburg': {
        'handler': hamburg_parse,
        'prefix': 'http://speiseplan.studierendenwerk-hamburg.de/de/',
        'canteens': {
            'armgartstrasse':       '590',
            'bergedorf':            '520',
            'berliner-tor':         '530',
            'botanischer-garten':   '560',
            'bucerius-law-school':  '410',
            'cafe-mittelweg':       '690',
            'cafe-cfel':            '680',
            'cafe-jungiusstrasse':  '610',
            'cafe-alexanderstrasse':'660',
            'campus':               '340',
            'finkenau':             '420',
            'geomatikum':           '540',
            'harburg':              '570',
            'hcu':                  '430',
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
    'darmstadt': {
        'handler': darmstadt_parse,
        'prefix': 'http://www.stwda.de/components/com_spk/',
        'canteens': {
            'stadtmitte':       'spk_Stadtmitte_print.php?ansicht=',
            'lichtwiese':       'spk_Lichtwiese_print.php?ansicht=',
            'schoefferstrasse': 'spk_Schoefferstrasse_print.php?ansicht=',
            'dieburg':          'spk_Dieburg_print.php?ansicht=',
            'haardtring':       'spk_Haardtring_print.php?ansicht=',
        }
    },
    'niederbayern_oberpfalz': {
        'handler': niederbayern_oberpfalz_parse,
        'prefix': 'http://www.stwno.de/infomax/daten-extern/csv/',
        'canteens': {
            'th-deggendorf':  'HS-DEG',
            'hs-landshut':    'HS-LA',
            'uni-passau':     'UNI-P',
            'oth-regensburg': 'HS-R-tag',
            'uni-regensburg': 'UNI-R',
        }
    },
}

from ostniedersachsen import register_canteens as register_ostniedersachsen
register_ostniedersachsen(providers)


def parse(provider, canteen, today=False):
    if provider not in providers:
        return False
    provider = providers[provider]
    if canteen not in provider['canteens']:
        return False
    canteen = provider['canteens'][canteen]
    if type(canteen) is not tuple:
        canteen = (canteen,)
    return provider['handler'](provider['prefix'] + canteen[0], today,
                               *canteen[1:], **provider.get('options', {}))
