#!/usr/bin/env python3
import sys

from lxml import etree

from config import parse
from utils import Request, NotFoundError


class SimulatedRequest(Request):
    def __init__(self):
        self.host = 'http://example.org'


try:
    document = parse(SimulatedRequest(), *sys.argv[1:])
    print(document)

    # check if the document is valid according to the schema
    schema = etree.XMLSchema(file = "open-mensa-v2.xsd")
    parser = etree.XMLParser(schema = schema)
    etree.fromstring(document.encode("utf-8"), parser)
except NotFoundError as e:
    print(e, file = sys.stderr)
    sys.exit(2)
except etree.XMLSyntaxError as e:
    print("The generated xml is not a valid openmensa document:", file = sys.stderr)
    print(e, file = sys.stderr)
    sys.exit(3)
