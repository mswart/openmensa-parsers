#!python3
import json


class Request(object):
    pass


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
            raise Redirect(code=301, location='/'.join([request.host, self.name, source,
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


class Source(object):
    def __init__(self, name, parser, handler, args=[], kwargs={}, default_feed='full'):
        self.name = name
        self.parser = parser
        self.handler = handler
        self.args = args
        self.kwargs = kwargs
        self.default_feed = default_feed

    def parse(self, request, feed):
        print(self.args)
        return self.handler(*self.args, today=feed == 'today.xml', **self.kwargs)

    def metadataList(self, request):
        return {self.name: '/'.join([request.host, self.parser.name, self.name, 'metadata.xml'])}


# exceptions:

class ParserError(Exception):
    pass


class NotFoundError(ParserError):
    pass


class ParserNotFound(NotFoundError):
    def __init__(self, name):
        NotFoundError.__init__(self, 'Unknown parser "{}"'.format(name))


class SourceNotFound(NotFoundError):
    def __init__(self, parser, name):
        NotFoundError.__init__(self, 'Unknown source "{}" for parser "{}"'.format(name, parser))


class Redirect(Exception):
    def __init__(self, code, location):
        self.code = code
        self.location = location
        Exception.__init__(self, '{} Redirect to {}'.format(code, location))
