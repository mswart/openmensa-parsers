import os
from config import parsers

base_directory = os.path.dirname(os.path.realpath(__file__))
snapshots_directory = os.path.join(base_directory, 'snapshots')


def get_snapshot_result_path(parser, canteen):
    return os.path.join(snapshots_directory, parser, canteen, 'full.xml')


def get_canteen_url(parser, canteen):
    parser = parsers[parser].sources[canteen]
    return parser.args[0]
