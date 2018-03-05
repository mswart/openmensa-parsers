import json
import os
from unittest import mock

import pytest

from config import parsers

base_directory = os.path.dirname(os.path.realpath(__file__))

parsers_to_test = [
    ('aachen', 'academica'),
]


@pytest.mark.parametrize("parser,canteen", parsers_to_test)
def test_parse_url(parser, canteen):
    result = parse_mocked(parser, canteen)
    with open(get_snapshot_result_path(parser, canteen), encoding='utf-8') as result_file:
        expected_result = result_file.read()
        assert result == expected_result


def parse_mocked(parser, canteen):
    snapshot_website_path = get_snapshot_website_path(parser, canteen)
    with open(snapshot_website_path) as snapshot_file:
        website_snapshots = json.load(snapshot_file)

        def mock_response(actual_url):
            class MockResponse:
                def read(self):
                    return website_snapshots[actual_url]

            return MockResponse()

    with mock.patch('urllib.request.urlopen', mock_response):
        return parsers[parser].parse('', canteen, 'full.xml')


def get_snapshot_website_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-website.json')


def get_snapshot_result_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-result.xml')
