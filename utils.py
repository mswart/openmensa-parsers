#!python3
import json


class Request(object):
    def __init__(self, eniron):
        self.host = eniron.get('wsgi.url_scheme', 'http') \
            + '://' \
            + eniron.get('HTTP_HOST', 'omfeeds.devtation.de') \
            + eniron.get('PATH_PREFIX', '')


class Parser(object):
    def __init__(self, name, handler=None, shared_prefix=None, shared_args=[], parent=None):
        self.name = name
        self.handler = handler or (parent and parent.handler)

        self.shared_prefix = (parent and parent.shared_prefix)
        if shared_prefix:
            self.shared_prefix = (self.shared_prefix or '') + shared_prefix
        self.shared_args = shared_args or (parent and parent.shared_args)
        self.sources = {}

    def define(self, name, suffix=None, args=[], extra_args={}):
        if args:
            source_args = self.shared_args + args
        else:
            source_args = [self.shared_prefix + suffix]
        self.sources[name] = Source(name, parser=self, handler=self.handler,
                                    args=source_args, kwargs=extra_args)

    def sub(self, name, *args, **kwargs):
        parser = Parser(self.name + '/' + name, *args, parent=self, **kwargs)
        self.sources[name] = parser
        return parser

    def parse(self, request, source, *args):
        if source in self.sources:
            return self.sources[source].parse(request, *args)
        elif source == 'index.json':
            return self.listSources(request)
        elif source[-4:] == '.xml' and source[:-4] in self.sources:
            raise Redirect(code=301, location='/'.join([request.host, self.name, source[:-4],
                                                        self.sources[source[:-4]].default_feed + '.xml']))
        else:
            raise SourceNotFound(self.name, source)

    def listSources(self, request):
        return json.dumps(self.metadataList(request), indent=2)

    def metadataList(self, request):
        metadatas = {}
        for source in self.sources.values():
            metadatas.update(source.metadataList(request))
        return metadatas


class CanteenPrefixer(object):
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix

    def parse(self, request, *args):
        raise Redirect(code=301, location='/'.join([request.host, self.prefix, self.name] + list(args)))


class ParserRenamer(object):
    def __init__(self, name, newname):
        self.name = name
        self.newname = newname

    def parse(self, request, source, *args):
        raise Redirect(code=301, location='/'.join([request.host, self.newname, source] + list(args)))


class Source(object):
    def __init__(self, name, parser, handler, args=[], kwargs={}, default_feed='full'):
        self.name = name
        self.parser = parser
        self.handler = handler
        self.args = args
        self.kwargs = kwargs
        self.default_feed = default_feed

    def parse(self, request, feed):
        return self.handler(*self.args, today=feed == 'today.xml', **self.kwargs)

    def metadataList(self, request):
        return {self.name: '/'.join([request.host, self.parser.name, self.name, 'metadata.xml'])}


# exceptions:

class ParserError(Exception):
    pass


class NotFoundError(ParserError):
    def __init__(self, reason):
        self.reason = reason
        super(NotFoundError, self).__init__(reason)


class ParserNotFound(NotFoundError):
    def __init__(self, name):
        super(ParserNotFound, self).__init__('Unknown parser "{}"'.format(name))


class SourceNotFound(NotFoundError):
    def __init__(self, parser, name):
        super(SourceNotFound, self).__init__('Unknown source "{}" for parser "{}"'.format(name, parser))


class Redirect(Exception):
    def __init__(self, code, location):
        self.code = code
        self.location = location
        Exception.__init__(self, '{} Redirect to {}'.format(code, location))
