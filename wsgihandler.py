import sys
import traceback
import re

from parse import parse
import utils

canteen_request = re.compile('/(?P<dirs>([\w-]+/)*[\w-]+)/(?P<file>[\w-]+.(xml|json))')


def handler(eniron, start_response):
    prefix = eniron.get('PATH_PREFIX', None)
    uri = eniron['PATH_INFO']
    if prefix and uri.startswith(prefix):
        uri = uri[len(prefix):]
    match = canteen_request.match(uri)
    if not match:
        start_response("404 Wrong Path", [("Content-type", 'application/xml; charset=utf-8')])
        return ['<xml version="1.0"><info>{provider}/{canteen}/{feed}.xml</info></xml>'.encode('utf8')]
    request = utils.Request(eniron)
    try:
        file = match.group('file')
        content = parse(request, *(match.group('dirs').split('/') + [file]))
        content = content.encode('utf8')
        if file.endswith(".json"):
            content_type = 'application/json'
        else:
            content_type = 'application/xml'
        start_response('200 OK', [('Content-Type', content_type + '; charset=utf-8'),
                                  ('Content-Length', str(len(content)))])
        return (content,)
    except utils.Redirect as e:
        start_response('301 Permanent Redirect', [('Location', e.location)])
        return ('',)
    except utils.ParserNotFound as e:
        start_response('404 Parser not found', [('Content-Type', 'text/plain; charset=utf-8')])
        return (e.reason,)
    except utils.SourceNotFound as e:
        start_response('404 Source not found', [('Content-Type', 'text/plain; charset=utf-8')])
        return (e.reason,)
    except utils.FeedNotFound as e:
        start_response('404 Feed not found', [('Content-Type', 'text/plain; charset=utf-8')])
        return (e.reason,)
    except utils.NotFoundError as e:
        start_response('404 Unknown file format', [('Content-Type', 'text/plain; charset=utf-8')])
        return (e.reason,)
    except Exception:
        traceback.print_exception(*sys.exc_info())
        start_response('500 Internal Server Error', [])
        return ('', )
