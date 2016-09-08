import pickle
import sys

from web_pyramid.web_pyramid.app_logic.similarity.analyzer import Analyzer, tt


if __name__ == '__main__':
    a = Analyzer()
    load = True

    if not load:
        print('Collecting links...')
        a.get_links(['olx', 'gumtree'], 'rent', 'mieszkania', 'Poznan', 'wielkopolskie')
        # , 'gumtree', 'otodom', 'gratka'
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
    l = a.process_similarity(0.5)
    a.print(l)
    print(a.get_links_list_with_titles(l))
