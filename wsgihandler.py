#!python3
from config import providers, parse
import re

canteen_request = re.compile('/(?P<provider>\w+)/(?P<canteen>[-_a-zA-Z0-9]+).xml')

def handler(eniron, start_response):
	prefix = eniron['PATH_PREFIX']
	uri = eniron['PATH_INFO']
	docroot = eniron['DOCUMENT_ROOT']
	if uri.startswith(prefix):
		uri = uri[len(prefix):]
	match = canteen_request.match(uri)
	if not match:
		start_response("200 Wrong Path", [("Content-type", 'application/xml; encoding=utf8')])
		return ['<xml version="1.0"><test/></xml>']
	elif match.group('provider') not in providers:
		start_response('404 Provider not found', [])
	elif match.group('canteen') not in providers[match.group('provider')]['canteens']:
		start_response('404 Canteen not found', [])
	else:
		try:
			content = parse(match.group('provider'), match.group('canteen'))
		except Exception as e:
			print(e)
			start_response('500 Internal Server Error', [])
			return
		content = content.encode('utf8')
		start_response('200 OK', [('Content-Type', 'application/xml; coding=utf-8l'), ('Content-length', str(len(content)))])
		return (content,)
