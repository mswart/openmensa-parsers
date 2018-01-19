import os
import requests_mock

from .parser import parse_url

base_directory = os.path.dirname(os.path.realpath(__file__))


def test_parse_url():
    url = 'http://www.studierendenwerk-aachen.de/speiseplaene/academica-w.html'
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
