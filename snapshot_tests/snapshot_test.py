import os

import pytest

from config import parsers
from .utils import get_snapshot_result_path, snapshots_directory

# List all snapshots subdirectories, e. g. `aachen/academica` becomes ("aachen", "academica").
parsers_to_test = [
    (parser, canteen)
    for parser in os.listdir(snapshots_directory)
    for canteen in os.listdir(os.path.join(snapshots_directory, parser))
]


@pytest.mark.parametrize("parser,canteen", parsers_to_test)
def test_parse_url(parser, canteen):
    result = parsers[parser].parse('', canteen, 'full.xml')
    with open(get_snapshot_result_path(parser, canteen), encoding='utf-8') as result_file:
        expected_result = result_file.read()
        assert result == expected_result


