#!python3
import re
import datetime

from utils import Parser, EsaySource, Source


class Canteen(EsaySource):
    def __init__(self, *args, location, needed_title, not_halle=False):
        super(Canteen, self).__init__(*args)
        self.location = location
        self.needed_title = needed_title
        self.not_halle = not_halle

    def parse_data(self, **kwargs):
        kwargs['selected_locations[]'] = self.location
        data = self.parse_remote('https://www.meine-mensa.de/speiseplan_iframe',
                                 args=kwargs)
        table = data.find('table', 'speiseplan')

        date = None
        pos = 0
        for tr in table.tbody.find_all('tr', recursive=False):
            if pos == 0:
                if self.needed_title:
                    assert self.needed_title in tr.text, tr.text
                else:
                    print(tr.text)
                pos += 1
                continue
            elif pos == 1:
                pos += 1
                continue
            if 'break' in tr.attrs.get('class', []):
                date = list(tr.find_all('td'))[1].text
                continue
            if 'empty_cell' in tr.attrs.get('class', []):
                continue
            tds = list(tr.find_all('td', recursive=False))
            category = tds[1].find('span', attrs={'class': 'npsble'}).text.strip() or 'Hauptessen'
            name = tds[2].find('img').attrs['alt'].strip()
            if not name:
                continue
            prices = {'student': tds[3].text, 'employee': tds[4].text, 'other': tds[5].text}
            self.feed.addMeal(date, category, name, prices=prices)

    def extract_metadata(self):
        url_template = 'http://www.studentenwerk-halle.de/hochschulgastronomie/{}/{}/'
        if self.not_halle:
            url = url_template.format(self.name, 'mensa-' + self.name)
        else:
            name = self.name
            if 'mensa' not in name:
                name = 'mensa-' + name
            url = url_template.format(self.parser.local_name, name)
        document = self.parse_remote(url)
        attachment = document.find(id='attachContact')

        canteen = self.feed
        canteen.name = document.find('li', attrs={'class': 'current'}).text
        canteen.availability = 'public'
        canteen.address = attachment.find(attrs={'class': 'address'}).text + ', ' + attachment.find(attrs={'class': 'city'}).text
        canteen.city = re.search('\d{5}\s+(?P<city>.+)', canteen.address).group('city')
        canteen.phone = attachment.find(attrs={'class': 'fon'}).text.split(':')[1].strip()
        #email_span = attachment.find(attrs={'class': 'email'})
        #if email_span:
        #    canteen.email = email_span.text

        script = document.find(id='attachMap').find('script').find_all(text=True)[0]
        match = re.search('\[\s*(?P<long>\d+\.\d+)\s*,\s*(?P<lat>\d+\.\d+)\s*]', script)
        canteen.location(match.group('lat'), match.group('long'))

    @Source.today_feed
    def today(self, request):
        day = datetime.datetime.now()
        self.parse_data(day=day.day, month=day.month, year=day.year)
        return self.feed.toXMLFeed()

    @Source.feed(name='thisWeek', priority=1, hour='8', retry='2 60')
    def thisWeek(self, request):
        day = datetime.datetime.now().isocalendar()
        self.parse_data(week=day[1], year=day[0])
        return self.feed.toXMLFeed()

    @Source.feed(name='nextWeek', priority=2, hour='9')
    def nextWeek(self, request):
        day = (datetime.datetime.now() + 7 * datetime.date.resolution).isocalendar()
        self.parse_data(week=day[1], year=day[0])
        return self.feed.toXMLFeed()


parser = Parser(name='halle', version=1.0)
Canteen('harzmensa', parser, location=3, needed_title='Harzmensa')
Canteen('weinbergmensa', parser, location=5, needed_title='Weinbergmensa')
#Canteen('cafebar-weinberg', parser, location=, needed_title='')
Canteen('tulpe', parser, location=10, needed_title='Mensa Tulpe')
Canteen('heidemensa', parser, location=17, needed_title='Heidemensa')
Canteen('burg', parser, location=12, needed_title='Mensa Burg')
Canteen('neuwerk', parser, location=9, needed_title='Neuwerk')
Canteen('franckesche-stiftungen', parser, location=14, needed_title='Franckesche Stiftungen')

#merseburg = parser.sub('merseburg')
Canteen('merseburg', parser, location=16, needed_title='Mensa Merseburg', not_halle=True)
#Canteen('cafebar-merseburg', merseburg, location=, needed_title=)

#dessau = parser.sub('dessau')
Canteen('dessau', parser, location=13, needed_title='Mensa Dessau', not_halle=True)

koethen = parser.sub('koethen')
Canteen('fasanerieallee', koethen, location=7, needed_title='Mensa Köthen')
#Canteen('lohmannstrasse', koethen, location=, needed_title=None)

#bernburg = parser.sub('bernburg')
Canteen('bernburg', parser, location=8, needed_title='Mensa Bernburg', not_halle=True)
