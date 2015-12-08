#!python3
import sys

from config import parse
from utils import Request, NotFoundError


class SimulatedRequest(Request):
    def __init__(self):
        self.host = 'http://example.org'


try:
    print(parse(SimulatedRequest(), *sys.argv[1:]))
except NotFoundError as e:
    print(e)
    sys.exit(2)
