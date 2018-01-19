import os
import requests_mock

from config import parsers
from .parser import parse_url

base_directory = os.path.dirname(os.path.realpath(__file__))

parser = parsers['aachen'].sources['academica']


def test_parse_url():
    url = parser.args[0]
    result = parse_mocked(url)

    with open(os.path.join(base_directory, 'snapshot-result.xml')) as result_file:
        expected_result = result_file.read()
        assert result == expected_result


def parse_mocked(url):
    with requests_mock.Mocker() as mocker:
        with open(os.path.join(base_directory, 'snapshot-website.html')) as html_file:
            html = html_file.read()
            mocker.get(url, text=html)
            return parse_url(url)
