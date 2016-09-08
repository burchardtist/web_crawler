from .app_logic.similarity.analyzer import Analyzer

use_mongo_cache = False
cache = None

if use_mongo_cache:
    from .app_logic.cache.mongo_cache import MongoCache
    cache = MongoCache()


def wrap(sources, offer_type, estate_type, city=None, voivodeship=None, similarity_threshold=0.5, room_difference=1,
         size_difference=0.1, price_difference=0.1):
    analyzer = Analyzer(similarity_threshold, price_difference, size_difference, room_difference)

    if cache is not None:
        saved_rooms, saved_urls = cache.get_collection(cache.get_hash_from_params(sources, offer_type, estate_type,
                                                                                  cache, voivodeship))

        if saved_rooms and saved_urls:
            analyzer.set_lists(saved_rooms, saved_urls)
        else:
            analyzer.get_links(sources, offer_type, estate_type, city, voivodeship)
            analyzer.get_rooms_async()

            rooms, urls = analyzer.get_lists()

            cache.save_collection(rooms, urls, cache.get_hash_from_params(sources, offer_type, estate_type, cache,
                                                                          voivodeship))
    else:
        analyzer.get_links(sources, offer_type, estate_type, city, voivodeship)
        analyzer.get_rooms_async()

    return analyzer.get_links_list_with_titles(analyzer.process_similarity())
