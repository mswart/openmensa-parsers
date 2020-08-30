#!/usr/bin/env python3

import os
import sys

from config import parsers
from .utils import get_canteen_url, get_snapshot_result_path


def generate_snapshot(parser, canteen):
    url = get_canteen_url(parser, canteen)
    result = parsers[parser].parse(url, canteen, 'full.xml')

    snapshot_result_path = get_snapshot_result_path(parser, canteen)
    os.makedirs(os.path.dirname(snapshot_result_path), exist_ok=True)
    with open(snapshot_result_path, 'w', encoding='utf-8') as result_file:
        result_file.write(result)

    print("Updated snapshots for {}/{}.".format(parser, canteen))


def main():
    if len(sys.argv) == 3:
        parser, canteen = sys.argv[1:3]
        generate_snapshot(parser, canteen)
    else:
        script_name = os.path.basename(sys.argv[0])
        print(
            "Wrong amount of arguments passed. \n"
            "Usage: `{0} <parser> <canteen>`.".format(script_name),
            file=sys.stderr
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
