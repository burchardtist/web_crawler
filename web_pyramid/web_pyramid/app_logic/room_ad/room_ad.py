from bs4 import BeautifulSoup
import urllib.request
import re
from datetime import datetime


def to_float(s):
    s = re.search('(\d+\s+)*\d+[.,]?\d{0,2}', s).group(0)
    s = re.sub('\s+', '', s)
    s = re.sub(',', '.', s)

    return float(s)


class GumtreeRoom:
    attributes_types = {
        'date_created': 0,
        'city': 1,
        'date_available': 3,
        'rooms_number': 5,
        'size': 7,
        'smoking': 10,
        'animals': 9,
    }

    def __init__(self, url, from_url=True):
        self.attributes = {
            'date_created': None,
            'city': '',
            'city_v': '',
            'street': '',
            'date_available': None,
            'rooms_number': '',
            'size': '',
            'smoking': None,
            'animals': None,

            'description': '',
            'price': '',
            'title': '',
            'user': ''
        }

        self.url = url
        soup = BeautifulSoup(urllib.request.urlopen(self.url) if from_url else self.url, 'html.parser')

        raw_attributes = soup.select('.selMenu .attribute')
        for attr, i in self.attributes_types.items():
            try:
                html_attr = raw_attributes[i]
                self.attributes[attr] = html_attr.select(".value")[0].text.strip()
            except IndexError:
                pass

        for x in ['animals', 'smoking']:
            if self.attributes[x]:
                self.attributes[x] =\
                    True if self.attributes[x].lower() == 'tak'\
                    else False

        for x in ['date_created', 'date_available']:
            if self.attributes[x]:
                date = self.attributes[x].rsplit('/')
                date = [int(x) for x in date]
                date = datetime(day=date[0], month=date[1], year=date[2])
                self.attributes[x] = date

        raw_city = self.attributes['city'].lower()
        m = re.findall('(\\w+)', raw_city)
        self.attributes['city'] = m[0]
        self.attributes['city_v'] = m[1]
        self.attributes['description'] = soup.select('.description')[0].getText().lower()

        raw_price = soup.select('.price .amount')[0].getText()
        raw_price = ''.join(raw_price.split())
        self.attributes['price'] = raw_price[:-2]

        self.attributes['title'] = soup.select('.myAdTitle')[0].getText().lower().strip()

        raw_username = soup.select('.username')[0].getText().lower().strip()
        m = re.match('(\\w+)', raw_username)
        self.attributes['user'] = m.group(1)


class OlxRoom:
    def __init__(self, url, from_url=True):
        self.attributes = {
            'date_created': None,
            'city': '',
            'city_v': '',
            'street': '',
            'date_available': None,
            'rooms_number': '',
            'size': '',
            'smoking': None,
            'animals': None,

            'description': '',
            'price': '',
            'title': '',
            'user': ''
        }

        self.url = url
        soup = BeautifulSoup(urllib.request.urlopen(self.url) if from_url else self.url, 'html.parser')

        raw_items = soup.select('.item')

        for item in raw_items:
            if item.select('th')[0].getText() == 'Liczba pokoi':
                raw = item.select('.value')[0].getText().strip()
                self.attributes['rooms_number'] = raw
            elif item.select('th')[0].getText() == 'Powierzchnia':
                raw = item.select('.value')[0].getText().strip()
                self.attributes['size'] = raw[:-2].strip()

        raw_price = soup.select('.pricelabel')[0].getText().strip()
        raw_price = "".join(raw_price.split())[:-2]
        self.attributes['price'] = raw_price

        self.attributes['title'] = soup.select('.offerheadinner h1')[0].getText().strip().lower()

        raw_location = soup.select('.offerheadinner .c2b')[0].getText().strip().lower()
        raw_location = raw_location.rsplit(',')
        raw_location = [x.strip(' ') for x in raw_location]
        self.attributes['city'] = raw_location[0]
        self.attributes['city_v'] = raw_location[1]
        self.attributes['street'] = raw_location[2]

        raw_date_c = soup.select('.offerheadinner .c62')[0].getText().strip()
        raw_date_c = raw_date_c.rsplit(',')
        time = re.findall('([0-9][0-9]:[0-9][0-9])', raw_date_c[0])[0]
        date = raw_date_c[1]
        self.attributes['date_created'] = '{} {}'.format(date, time)

        self.attributes['user'] = soup.select('.userdetails span')[0].getText().strip().lower()

        self.attributes['description'] = soup.select('#textContent')[0].getText().lower().strip()


class OtodomRoom:
    def __init__(self, url, from_url=True):
        self.attributes = {
            'date_created': None,
            'city': '',
            'city_v': '',
            'street': '',
            'date_available': None,
            'rooms_number': '',
            'size': '',
            'smoking': None,
            'animals': None,

            'description': '',
            'price': '',
            'title': '',
            'user': ''
        }

        self.url = url
        soup = BeautifulSoup(urllib.request.urlopen(self.url) if from_url else self.url, 'html.parser')

        self.attributes['description'] = soup.select('.text-contents')
        self.attributes['description'] = self.attributes['description'][0].text
        self.attributes['description'] = re.sub('\s+', ' ', self.attributes['description'])

        num_attributes = soup.select('.main-list')[0].text
        num_attributes = num_attributes.split('\n')

        for na in num_attributes:
            if na.startswith('cena'):
                self.attributes['price'] = to_float(na)
            elif na.startswith('powierzchnia'):
                self.attributes['size'] = to_float(na)
            elif na.startswith('liczba pokoi'):
                self.attributes['rooms_number'] = int(re.search('\d+', na).group(0))

        # TODO other, unused currently attributes


class GratkaRoom:
    def __init__(self, url, from_url=True):
        self.attributes = {
            'date_created': None,
            'city': '',
            'city_v': '',
            'street': '',
            'date_available': None,
            'rooms_number': '',
            'size': '',
            'smoking': None,
            'animals': None,

            'description': '',
            'price': '',
            'title': '',
            'user': ''
        }

        self.url = url
        soup = BeautifulSoup(urllib.request.urlopen(self.url) if from_url else self.url, 'html.parser')

        self.attributes['description'] = soup.select('.opis')
        self.attributes['description'] = self.attributes['description'][0].text
        self.attributes['description'] = re.sub('\s+', ' ', self.attributes['description'])
        if self.attributes['description'].startswith(' Opis dodatkowy'):
            self.attributes['description'] = self.attributes['description'][15:]

        num_attributes = soup.select('#dane-podstawowe')[0].text.split('\n')
        num_attributes = list(filter(lambda a: a != '', num_attributes))

        for i in range(len(num_attributes)):
            if num_attributes[i] == 'Cena':
                self.attributes['price'] = to_float(num_attributes[i+1])
            elif num_attributes[i] == 'Powierzchnia':
                self.attributes['size'] = to_float(num_attributes[i+1])
            elif num_attributes[i] == 'Liczba pokoi':
                self.attributes['rooms_number'] == int(re.search('\d+', num_attributes[i+1]).group(0))

        # TODO other, unused currently attributes


if __name__ == '__main__':
    # url_ = 'http://www.gumtree.pl/a-mieszkania-i-domy-do-wynajecia/krakow/super-oferta-3+pokojowe-69-m2-ip-ul-turka-ok-saska-lipska-piekne-i-zadbane/1001721891170910514696009'
    # gt = GumtreeRoom(url_)

    # url_ = 'http://olx.pl/oferta/mieszkania-blisko-pg-i-gumed-2-niezalezne-pokoje-gdansk-brzezno-CID3-IDh3gTw.html#2244b69db2;promoted'
    # olx = OlxRoom(url_)

    # url_ = 'https://otodom.pl/oferta/piatkowo-batorego-63-1m-ii-pietro-bez-posrednikow-ID3133O.html#465ffef225'
    # od = OtodomRoom(url_)

    url_ = 'http://dom.gratka.pl/tresc/401-69501979-wielkopolskie-poznan-piatkowo-os-stefana-batorego.html'
    gr = GratkaRoom(url_)

    print('ok')