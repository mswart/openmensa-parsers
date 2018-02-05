import json
import os
import sys
from unittest import mock
from urllib.request import urlopen

from config import parsers
from parsers.tests.regression_test import get_canteen_url, \
    get_snapshot_result_path, \
    get_snapshot_website_path, \
    parse_mocked, parsers_to_test

base_directory = os.path.dirname(os.path.realpath(__file__))


def generate_all_snapshots():
    for parser, canteen in parsers_to_test:
        generate_snapshot(parser, canteen)


def generate_snapshot(parser, canteen):
    intercepted_requests = {}

    def intercept_request(requested_url):
        response = urlopen(requested_url)

        html = response.read()
        intercepted_requests[requested_url] = html.decode('utf-8')

        # cannot return original response, because read() has side effects on it
        return urlopen(requested_url)

    with mock.patch('urllib.request.urlopen', intercept_request):
        url = get_canteen_url(parser, canteen)
        parsers[parser].parse(url, canteen, 'full.xml')

    snapshot_website_path = get_snapshot_website_path(parser, canteen)
    with open(snapshot_website_path, 'w', encoding='utf-8') as file:
        json.dump(intercepted_requests, file)

    snapshot_result_path = get_snapshot_result_path(parser, canteen)
    with open(snapshot_result_path, 'w', encoding='utf-8') as result_file:
        result = parse_mocked(parser, canteen)
        result_file.write(result)

    print("Updated snapshots for {}/{}.".format(parser, canteen))


def main():
    if len(sys.argv) < 2:
        usage_hint = "Usage: `update_snapshots.py <parser> <canteen>`"
        print("Missing arguments.", usage_hint)

    if len(sys.argv) == 2 and sys.argv[1] == '--all':
        generate_all_snapshots()
    elif len(sys.argv == 3):
        parser, canteen = sys.argv[1:3]
        generate_snapshot(parser, canteen)


if __name__ == '__main__':
    main()
