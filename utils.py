import os.path
from urllib.request import urlopen
from urllib.parse import urlencode
import json

from bs4 import BeautifulSoup

from pyopenmensa.feed import LazyBuilder, Feed


class Request(object):
    def __init__(self, eniron):
        self.host = eniron.get('wsgi.url_scheme', 'http') \
            + '://' \
            + eniron.get('HTTP_HOST', 'omfeeds.devtation.de') \
            + eniron.get('PATH_PREFIX', '')


class Parser(object):
    def __init__(self, name, handler=None, shared_prefix=None, shared_args=[], parent=None, version=None):
        self.local_name = name
        self.name = name
        self.version = version
        if parent:
            parent.sources[name] = self
            self.name = parent.name + '/' + self.name
            self.version = self.version or parent.version
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
        HandlerSource(name, parser=self, handler=self.handler,
                      args=source_args, kwargs=extra_args)

    def sub(self, name, *args, **kwargs):
        return Parser(name, *args, parent=self, **kwargs)

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
    def __init__(self, name, parser, default_feed='full'):
        self.name = name
        self.parser = parser
        self.default_feed = default_feed
        parser.sources[name] = self

    def parse(self, request, feed):
        raise NotImplementedError('Needs to be done by parser')

    def metadataList(self, request):
        return {self.name: '/'.join([request.host, self.parser.name, self.name, 'metadata.xml'])}

    @classmethod
    def feed(cls, name, hour, url=None, priority=0, source=None, dayOfMonth='*', dayOfWeek='*', minute='0', retry=None):
        def decorator(fnc):
            fnc.name = name
            fnc.url = url or cls.buildFeedUrl
            fnc.priority = priority
            fnc.source = source
            fnc.hour = hour
            fnc.minute = minute
            fnc.dayOfMonth = dayOfMonth
            fnc.dayOfWeek = dayOfWeek
            fnc.retry = retry
            return fnc
        return decorator

    @staticmethod
    def today_feed(fnc):
        return Source.feed(name='today', hour='8-14')(fnc)

    @staticmethod
    def full_feed(fnc):
        return Source.feed(name='full', hour='8')(fnc)

    @staticmethod
    def buildFeedUrl(name, source, request):
        return '/'.join([request.host, source.parser.name, source.name, name + '.xml'])


class EasySource(Source):
    @property
    def feed(self):
        if not hasattr(self, '_feed'):
            self._feed = LazyBuilder(version=str(self.parser.version))
        return self._feed

    def parse(self, request, feed):
        # Reset feed before every request
        if hasattr(self, '_feed'):
            del self._feed

        if feed == 'metadata.xml':
            return self.metadata(request)
        elif os.path.splitext(feed)[1] != '.xml':
            raise NotFoundError('unknown file')
        feedname = os.path.splitext(feed)[0]
        for feed in self.feeds():
            if feed.name == feedname:
                return feed(self, request)
        raise FeedNotFound(feedname, self.name, self.parser.name)

    def parse_remote(self, url, args=None, tls_context=None):
        if args is not None:
            args = urlencode(args).encode('utf-8')
        return BeautifulSoup(urlopen(url, data=args, context=tls_context).read(), 'lxml')

    def metadata(self, request):
        self.extract_metadata()
        self.define_feeds(request)
        return self.feed.toXMLFeed()

    def feeds(self):
        for obj in type(self).__dict__.values():
            if hasattr(obj, 'name') and hasattr(obj, 'url'):
                yield obj

    def define_feeds(self, request):
        for feed in self.feeds():
            args = dict(feed.__dict__)
            if callable(args['url']):
                args['url'] = args['url'](args['name'], self, request)
            self.feed.define(**args)

    def extract_metadata(self):
        """Can be implemented to provide more information about the canteen."""
        pass


class HandlerSource(Source):
    def __init__(self, name, parser, handler, args=[], kwargs={}, default_feed='full'):
        super(HandlerSource, self).__init__(name, parser, default_feed=default_feed)
        self.handler = handler
        self.args = args
        self.kwargs = kwargs

    def metadata(self, request):
        meta = LazyBuilder(version=self.parser.version)

        meta.feeds.append(Feed(
            name='today',
            hour='8-14',
            url='/'.join([request.host, self.parser.name, self.name, 'today.xml']),
            priority=0,
            source=None,
            dayOfMonth='*',
            dayOfWeek='*',
            minute='0',
            retry=None
        ))

        meta.feeds.append(Feed(
            name='full',
            hour='8',
            url='/'.join([request.host, self.parser.name, self.name, 'full.xml']),
            priority=0,
            source=None,
            dayOfMonth='*',
            dayOfWeek='*',
            minute='0',
            retry=None
        ))

        return meta.toXMLFeed()

    def parse(self, request, feed):
        if feed == 'metadata.xml':
            return self.metadata(request)

        return self.handler(*self.args, today=feed == 'today.xml', **self.kwargs)


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


class FeedNotFound(NotFoundError):
    def __init__(self, name, source, parser):
        super(FeedNotFound, self).__init__('Unknown feed "{}" for "{}" of "{}"'.format(name, source, parser))


class Redirect(Exception):
    def __init__(self, code, location):
        self.code = code
        self.location = location
        Exception.__init__(self, '{} Redirect to {}'.format(code, location))
