import re
import datetime

from utils import Parser, EasySource, Source


class Canteen(EasySource):
    def __init__(self, *args, location, needed_title, meta):
        super(Canteen, self).__init__(*args)
        self.location = location
        self.needed_title = needed_title
        self.meta = meta

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
            noteSpans = tds[1].find_all(['span'], attrs={'style': 'font-weight: normal; font-size: 10px;cursor:pointer;'})
            notes = set()
            for span in noteSpans:
              note = span.get('title')
              if note != '':
                notes.add(note)
            prices = {'student': tds[3].text, 'employee': tds[4].text, 'other': tds[5].text}
            self.feed.addMeal(date, category, name, notes=notes, prices=prices)

    def extract_metadata(self):
        url_template = 'http://www.studentenwerk-halle.de/mensen-cafebars/{}/'
        url = url_template.format(self.meta)
        document = self.parse_remote(url)

        contactInfo = document.find('div', attrs={'itemprop': 'areaServed'})
        member = document.find('div', attrs={'itemprop': 'member'})
        address = contactInfo.find(attrs={'itemprop': 'address'})
        street = address.find(attrs={'itemprop': 'streetAddress'}).text
        postalCode = address.find(attrs={'itemprop': 'postalCode'}).text
        city = address.find(attrs={'itemprop': 'addressLocality'}).text

        canteen = self.feed
        canteen.name = contactInfo.find(attrs={'itemprop': 'name'}).text
        canteen.availability = 'public'
        canteen.address = '{}, {} {}'.format(street, postalCode, city)
        canteen.city = city
        canteen.phone = member.find(attrs={'itemprop': 'telephone'}).text

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
Canteen('harzmensa', parser, location=3, needed_title='Harzmensa', meta='mensen-in-halle/harzmensa')
Canteen('weinbergmensa', parser, location=5, needed_title='Weinbergmensa', meta='mensen-in-halle/weinbergmensa-mit-cafebar')
#Canteen('cafebar-weinberg', parser, location=, needed_title='', meta='')
Canteen('tulpe', parser, location=10, needed_title='Mensa Tulpe', meta='mensen-in-halle/mensa-tulpe')
Canteen('heidemensa', parser, location=17, needed_title='Heidemensa', meta='mensen-in-halle/heidemensa-mit-cafebar')
Canteen('burg', parser, location=12, needed_title='Mensa Burg', meta='mensen-in-halle/mensa-burg')
Canteen('neuwerk', parser, location=9, needed_title='Neuwerk', meta='mensen-in-halle/mensa-neuwerk')
Canteen('franckesche-stiftungen', parser, location=14, needed_title='Franckesche Stiftungen', meta='mensen-in-halle/mensa-franckesche-stiftungen')

#merseburg = parser.sub('merseburg')
Canteen('merseburg', parser, location=16, needed_title='Mensa Merseburg', meta='mensa-merseburg-mit-cafebar')
#Canteen('cafebar-merseburg', merseburg, location=, needed_title=)

#dessau = parser.sub('dessau')
Canteen('dessau', parser, location=13, needed_title='Mensa Dessau', meta='mensa-dessau')

#koethen = parser.sub('koethen')
Canteen('fasanerieallee', parser, location=7, needed_title='Mensa Köthen', meta='mensen-in-koethen/mensa-fasanerieallee')
#Canteen('lohmannstrasse', koethen, location=, needed_title=None)

#bernburg = parser.sub('bernburg')
Canteen('bernburg', parser, location=8, needed_title='Mensa Bernburg', meta='mensa-bernburg')
