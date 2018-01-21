import os
from urllib.request import urlretrieve

from parsers.tests.regression_test import get_canteen_url, \
    get_snapshot_result_path, \
    get_snapshot_website_path, \
    parse_mocked, \
    parsers_to_test

base_directory = os.path.dirname(os.path.realpath(__file__))


def generate_all_snapshots(canteens):
    for (parser, canteen) in canteens:
        url = get_canteen_url(parser, canteen)

        snapshot_website_path = get_snapshot_website_path(parser, canteen)
        if not os.path.exists(os.path.dirname(snapshot_website_path)):
            os.makedirs(os.path.dirname(snapshot_website_path))
        urlretrieve(url, snapshot_website_path)

        snapshot_result_path = get_snapshot_result_path(parser, canteen)
        with open(snapshot_result_path, 'w', encoding='utf-8') as result_file:
            result = parse_mocked(parser, canteen)
            result_file.write(result)

        print("Updated snapshots for {}/{}.".format(parser, canteen))


if __name__ == '__main__':
    generate_all_snapshots(parsers_to_test)
