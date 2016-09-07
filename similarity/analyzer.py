import pickle

from room_ad.room_ad import OlxRoom, GumtreeRoom
from crawler.link_fetcher import LinkFetcher
from crawler.links_params import links, cast_params
from nlp_analyzer.tfidf_analyzer import TfidfSimilarity
from crawler.document_fetcher import HtmlFetcher


class Analyzer:
    def __init__(self):
        self._url_list = {}
        self._rooms = []

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
                        print(len(url_list))
                    except:
                        continue
            elif source == 'gumtree':
                for url in self._url_list[source]:
                    try:
                        self._rooms.append(GumtreeRoom(url).attributes)
                        url_list.append(url)
                        print(len(url_list))
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
                for url, html in zip(self._url_list[source], async_html_fetch.get_all_documents()):
                    try:
                        self._rooms.append(OlxRoom(html, False).attributes)
                        url_list.append(url)
                        print(len(url_list))
                    except:
                        continue
            elif source == 'gumtree':
                async_html_fetch.load_all_documents(self._url_list[source])
                for url, html in zip(self._url_list[source], async_html_fetch.get_all_documents()):
                    try:
                        self._rooms.append(GumtreeRoom(html, False).attributes)
                        url_list.append(url)
                        print(len(url_list))
                    except:
                        continue
            else:
                raise NotImplementedError()

        self._url_list = url_list

        return len(url_list)

    def values_difference(self, attributes_list, attribute, index_1, index_2, allowed_difference=0.1):
        a = attributes_list[index_1][attribute]
        b = attributes_list[index_2][attribute]

        if isinstance(a, str) or isinstance(b, str):
            a = float(a)
            b = float(b)

        return abs(a - b) / (a if a > b else b) <= allowed_difference

    def values_difference_int(self, attributes_list, attribute, index_1, index_2, allowed_difference=1):
        a = attributes_list[index_1][attribute]
        b = attributes_list[index_2][attribute]

        if isinstance(a, str) or isinstance(b, str):
            a = int(a)
            b = int(b)

        return abs(a - b) <= allowed_difference

    def process_similarity(self, threshold=0.95):
        tfidf_analyzer = TfidfSimilarity()
        print("Tfidf...")
        tfidf_analyzer.analyze_documents([e['description'] for e in self._rooms])
        similar_list = tfidf_analyzer.find_similar(threshold)

        similar_list = list(filter(lambda r: self.values_difference(self._rooms, 'price', r[0], r[1]), similar_list))
        similar_list = list(filter(lambda r: self.values_difference(self._rooms, 'size', r[0], r[1]), similar_list))
        #similar_list = list(filter(lambda r: self.values_difference_int(self._rooms, 'rooms_number', r[0], r[1]),
        #                           similar_list))

        similar_list_urls = list(map(lambda d: (self._url_list[d[0]], self._url_list[d[1]]), similar_list))

        for pair in similar_list_urls:
            print(pair)

        return similar_list


if __name__ == '__main__':
    a = Analyzer()
    load = True

    if not load:
        print('Collecting links...')
        a.get_links(['olx', 'gumtree'], 'rent', 'mieszkania', 'Poznan', 'wielkopolskie')
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
    a.process_similarity()
