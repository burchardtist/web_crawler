import pickle
import re

from ..crawler.document_fetcher import HtmlFetcher
from ..crawler.link_fetcher import LinkFetcher
from ..crawler.links_params import links, cast_params
from ..room_ad.room_ad import OlxRoom, GumtreeRoom, OtodomRoom, GratkaRoom

from ..nlp_analyzer.tfidf_analyzer import TfidfSimilarity


class Analyzer:
    def __init__(self, similarity_threshold=0.5, price_difference=0.1, size_difference=0.1, room_difference=1):
        self._url_list = {}
        self._rooms = []

        self.similarity_threshold = similarity_threshold
        self.price_difference = price_difference
        self.size_difference = size_difference
        self.room_difference = room_difference

    def get_links(self, sources, offer_type, estate_type, city=None, voivodeship=None):
        self._url_list = {}
        self._rooms = []

        for source in sources:
            link_fetch = LinkFetcher(links[source]['start_url'], links[source]['base_url'],
                                     links[source]['offer_pattern'], links[source]['page_pattern'],
                                     cast_params(source, estate_type, offer_type, city, voivodeship))
            link_fetch.process()
            self._url_list[source] = link_fetch.get_collected_links()

        return len(self._url_list)

    def get_rooms(self):
        url_list = []

        for source in self._url_list:
            if source == 'olx':
                for url in self._url_list[source]:
                    try:
                        self._rooms.append(OlxRoom(url).attributes)
                        url_list.append(url)
                    except:
                        continue
            elif source == 'gumtree':
                for url in self._url_list[source]:
                    try:
                        self._rooms.append(GumtreeRoom(url).attributes)
                        url_list.append(url)
                    except:
                        continue
            elif source == 'otodom':
                for url in self._url_list[source]:
                    try:
                        self._rooms.append(OtodomRoom(url).attributes)
                        url_list.append(url)
                    except:
                        continue
            elif source == 'gratka':
                for url in self._url_list[source]:
                    try:
                        self._rooms.append(GratkaRoom(url).attributes)
                        url_list.append(url)
                    except:
                        continue
            else:
                raise NotImplementedError()

        self._url_list = url_list

        return len(url_list)

    def get_rooms_async(self):
        async_html_fetch = HtmlFetcher()

        url_list = []

        for source in self._url_list:
            if source == 'olx':
                async_html_fetch.load_all_documents(self._url_list[source])
                for html in async_html_fetch.get_all_documents():
                    try:
                        self._rooms.append(OlxRoom(html['html'], False).attributes)
                        url_list.append(html['url'])
                    except:
                        continue
            elif source == 'gumtree':
                async_html_fetch.load_all_documents(self._url_list[source])
                for html in async_html_fetch.get_all_documents():
                    try:
                        self._rooms.append(GumtreeRoom(html['html'], False).attributes)
                        url_list.append(html['url'])
                    except:
                        continue
            elif source == 'otodom':
                async_html_fetch.load_all_documents(self._url_list[source])
                for html in async_html_fetch.get_all_documents():
                    try:
                        self._rooms.append(OtodomRoom(html['html'], False).attributes)
                        url_list.append(html['url'])
                    except:
                        continue
            elif source == 'gratka':
                async_html_fetch.load_all_documents(self._url_list[source])
                for html in async_html_fetch.get_all_documents():
                    try:
                        self._rooms.append(GratkaRoom(html['html'], False).attributes)
                        url_list.append(html['url'])
                    except:
                        continue
            else:
                raise NotImplementedError()

        self._url_list = url_list

        return len(url_list)

    def values_difference(self, attributes_list, attribute, index_1, index_2, allowed_difference=0.1):
        a = attributes_list[index_1][attribute]
        b = attributes_list[index_2][attribute]

        if a is None or b is None:
            return True

        try:
            if isinstance(a, str):
                a = self._to_float(a)
            if isinstance(b, str):
                b = self._to_float(b)
        except:
            return True  # value unknown, leave it as it is

        return abs(a - b) / (a if a > b else b) <= allowed_difference

    def _to_float(self, s):
        s = re.search('(\d+\s+)*\d+[.,]?\d{0,2}', s).group(0)
        s = re.sub('\s+', '', s)
        s = re.sub(',', '.', s)

        return float(s)

    def _to_int(self, s):
        return int(re.search('\d+', s).group(0))

    def values_difference_int(self, attributes_list, attribute, index_1, index_2, allowed_difference=1):
        a = attributes_list[index_1][attribute]
        b = attributes_list[index_2][attribute]

        try:
            if isinstance(a, str):
                a = self._to_int(a)
            if isinstance(b, str):
                b = self._to_int(b)
        except:
            return True

        return abs(a - b) <= allowed_difference

    def process_similarity(self, threshold=None):
        threshold = self.similarity_threshold if threshold is None or not isinstance(threshold, float) else threshold

        tfidf_analyzer = TfidfSimilarity()
        tfidf_analyzer.analyze_documents([e['description'] for e in self._rooms])
        similar_list = tfidf_analyzer.find_similar(threshold)

        similar_list = list(filter(lambda r: self.values_difference(self._rooms, 'price', r[0], r[1],
                                                                    self.price_difference), similar_list))
        similar_list = list(filter(lambda r: self.values_difference(self._rooms, 'size', r[0], r[1],
                                                                    self.size_difference), similar_list))
        similar_list = list(filter(lambda r: self.values_difference_int(self._rooms, 'rooms_number', r[0], r[1],
                                                                        self.room_difference), similar_list))

        similar_list = tfidf_analyzer.sort_by_similarity(similar_list)

        return similar_list

    def get_links_list(self, similar_list):
        return list(map(lambda d: (self._url_list[d[0]], self._url_list[d[1]]), similar_list))

    def get_links_list_with_titles(self, similar_list):
        return list(map(lambda d: ({'url': self._url_list[d[0]], 'title': self._rooms[d[0]]['title']},
                                   {'url': self._url_list[d[1]], 'title': self._rooms[d[1]]['title']}), similar_list))

    def print(self, similar_list):
        for pair in similar_list:
            print(self._url_list[pair[0]], self._url_list[pair[1]], self._rooms[pair[0]]['price'],
                  self._rooms[pair[1]]['price'], self._rooms[pair[0]]['size'], self._rooms[pair[1]]['size'],
                  self._rooms[pair[0]]['rooms_number'], self._rooms[pair[1]]['rooms_number'])

    def get_lists(self):
        return self._rooms, self._url_list

    def set_lists(self, rooms, urls):
        self._rooms = rooms
        self._url_list = urls


def tt(ndlist):
    return list(map(lambda n: (n[0], n[1]), ndlist))


if __name__ == '__main__':
    a = Analyzer()
    load = False

    if not load:
        print('Collecting links...')
        a.get_links(['olx', 'gumtree', 'otodom'], 'rent', 'mieszkania', 'Poznan', 'wielkopolskie')
        print('Getting rooms')
        a.get_rooms_async()

        rooms = open("rooms.pckl", "wb")
        urls = open("urls.pckl", "wb")

        pickle.dump(a._rooms, rooms)
        pickle.dump(a._url_list, urls)

        rooms.close()
        urls.close()
    else:
        rooms = open("rooms.pckl", "rb")
        urls = open("urls.pckl", "rb")

        a._rooms = pickle.load(rooms)
        a._url_list = pickle.load(urls)

        rooms.close()
        urls.close()

    print('Similarity...')
    a_1 = set(tt(a.process_similarity(0.6)))
    # print(len(a.process_similarity(0.9)))
    # print(len(a.process_similarity(0.85)))
    a_2 = set(tt(a.process_similarity(0.5)))

    l = list(a_2.difference(a_1))
    a.print(l)


