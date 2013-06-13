#!python3
import sys
import traceback
import re

from config import providers, parse

canteen_request = re.compile('/(?P<provider>\w+)/(?P<canteen>[-_a-zA-Z0-9]+)(?P<today>/today)?.xml')


def handler(eniron, start_response):
    prefix = eniron.get('PATH_PREFIX', None)
    uri = eniron['PATH_INFO']
    if prefix and uri.startswith(prefix):
        uri = uri[len(prefix):]
    match = canteen_request.match(uri)
    if not match:
        start_response("404 Wrong Path", [("Content-type", 'application/xml; charset=utf-8')])
        return ['<xml version="1.0"><info>{provider}/{canteen}.xml</info></xml>']
    elif match.group('provider') not in providers:
        start_response('404 Provider not found', [])
    elif match.group('canteen') not in providers[match.group('provider')]['canteens']:
        start_response('404 Canteen not found', [])
    else:
        try:
            content = parse(match.group('provider'), match.group('canteen'),
                            bool(match.group('today')))
        except Exception:
            traceback.print_exception(*sys.exc_info())
            start_response('500 Internal Server Error', [])
            return
        content = content.encode('utf8')
        start_response('200 OK', [('Content-Type', 'application/xml; charset=utf-8'),
                                  ('Content-length', str(len(content)))])
        return (content,)
