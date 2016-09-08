from .app_logic.similarity.analyzer import Analyzer


def wrap(sources, offer_type, estate_type, city=None, voivodeship=None, similarity_threshold=0.5, room_difference=1,
         size_difference=0.1, price_difference=0.1):
    analyzer = Analyzer(similarity_threshold, price_difference, size_difference, room_difference)
    analyzer.get_links(sources, offer_type, estate_type, city, voivodeship)
    analyzer.get_rooms_async()

    return analyzer.get_links_list_with_titles(analyzer.process_similarity())
