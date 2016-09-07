from room_ad.room_ad import OlxRoom, GumtreeRoom
from crawler.link_fetcher import LinkFetcher
from crawler.links_params import links, cast_params
from nlp_analyzer.tfidf_analyzer import TfidfSimilarity

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
            self._url_list += link_fetch.get_collected_links()

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
            else:
                raise NotImplementedError()

