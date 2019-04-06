import os

import pytest

from config import parsers

base_directory = os.path.dirname(os.path.realpath(__file__))

parsers_to_test = [
    ('aachen', 'academica'),
]


@pytest.mark.parametrize("parser,canteen", parsers_to_test)
def test_parse_url(parser, canteen):
    result = parsers[parser].parse('', canteen, 'full.xml')
    with open(get_snapshot_result_path(parser, canteen), encoding='utf-8') as result_file:
        expected_result = result_file.read()
        assert result == expected_result


def get_snapshot_result_path(parser, canteen):
    return os.path.join(base_directory, 'snapshots', parser, canteen, 'snapshot-result.xml')
