#!/usr/bin/env python3
import sys

from config import parsers
from utils import Request, NotFoundError, ParserNotFound


def parse(request, parser_name, *args):
    if parser_name in parsers:
        return parsers[parser_name].parse(request, *args)
    else:
        raise ParserNotFound(parser_name)


class SimulatedRequest(Request):
    def __init__(self):
        self.host = 'http://example.org'


if __name__ == '__main__':
    try:
        print(parse(SimulatedRequest(), *sys.argv[1:]))
    except NotFoundError as e:
        print(e)
        sys.exit(2)
