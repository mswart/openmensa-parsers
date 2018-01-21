import importlib
import os

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
        assert result == expected_result, ("Actual result:\n"
                                           + result
                                           + "\n------ Diff: ------\n")


def parse_mocked(parser, canteen):
    canteen_url = get_canteen_url(parser, canteen)
    with open(get_snapshot_website_path(parser, canteen), encoding='utf-8') as html_file:
        html = html_file.read()

        mock_request(parser, canteen_url, html)

        return parsers[parser].parse('', canteen, 'full.xml')


def mock_request(module, expected_url, response):
    def mock_response(actual_url):
        class MockResponse:
            def read(self):
                return response

        assert actual_url == expected_url
        return MockResponse()

    parser_import = importlib.import_module('parsers.' + module)
    parser_import.urlopen = mock_response


def get_canteen_url(parser, canteen):
    parser = parsers[parser].sources[canteen]
    return parser.args[0]


def get_snapshot_website_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-website.html')


def get_snapshot_result_path(parser, canteen):
    return os.path.join(base_directory, parser, canteen, 'snapshot-result.xml')
