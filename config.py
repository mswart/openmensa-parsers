import importlib

from utils import ParserNotFound

modules = [
    'aachen',
    'dresden',
    'hamburg',
    'hannover',
    'karlsruhe',
    'leipzig',
    'magdeburg',
    'muenchen',
    'marburg',
    'niederbayern_oberpfalz',
    'ostniedersachsen',
    'wuerzburg',
]


parsers = {}

for module in modules:
    parser = importlib.import_module(module).parser
    parsers[parser.name] = parser


def parse(request, parser_name, *args):
    if parser_name in parsers:
        return parsers[parser_name].parse(request, *args)
    else:
        raise ParserNotFound(parser_name)
