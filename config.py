import importlib

from utils import CanteenPrefixer, ParserRenamer

cities = [
    'aachen',
    'chemnitz_zwickau',
    'darmstadt',
    'dresden',
    'duesseldorf',
    'erlangen_nuernberg',
    'halle',
    'hamburg',
    'hannover',
    'karlsruhe',
    'leipzig',
    'magdeburg',
    'muenchen',
    'marburg',
    'niederbayern_oberpfalz',
    'ostniedersachsen',
    'siegen',
    'wuerzburg',
    'rostock',
]


def register_all_parsers(module_list):
    registered_parsers = {}

    def register_parser(parser):
        registered_parsers[parser.name] = parser

    for module in module_list:
        register_parser(importlib.import_module(f'parsers.{module}').parser)

    register_parser(CanteenPrefixer('braunschweig', 'ostniedersachsen'))
    register_parser(ParserRenamer('clausthal', 'ostniedersachsen'))
    register_parser(CanteenPrefixer('hildesheim', 'ostniedersachsen'))
    register_parser(CanteenPrefixer('suderburg', 'ostniedersachsen'))
    register_parser(CanteenPrefixer('wolfenbuettel', 'ostniedersachsen'))
    register_parser(CanteenPrefixer('holzminden', 'ostniedersachsen'))
    register_parser(CanteenPrefixer('lueneburg', 'ostniedersachsen'))

    return registered_parsers


parsers = register_all_parsers(cities)
