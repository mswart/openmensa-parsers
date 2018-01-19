import os

import pytest
import requests_mock

from config import parsers

base_directory = os.path.dirname(os.path.realpath(__file__))

parsers_to_test = [
    ('aachen', 'academica'),
]


@pytest.mark.parametrize("parser,canteen", parsers_to_test)
def test_parse_url(parser, canteen):
    result = parse_mocked(parser, canteen)

    with open(get_snapshot_result_path(parser, canteen)) as result_file:
        expected_result = result_file.read()
        assert result == expected_result


def parse_mocked(parser, canteen):
    url = get_canteen_url(parser, canteen)
    with requests_mock.Mocker() as mocker:
        with open(get_snapshot_website_path(parser, canteen)) as html_file:
            html = html_file.read()
            mocker.get(url, text=html)
            return parsers[parser].parse('', canteen, 'full.xml')


def get_canteen_url(parser, canteen):
    parser = parsers[parser].sources[canteen]
    return parser.args[0]


def get_snapshot_website_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-website.html')


def get_snapshot_result_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-result.xml')
