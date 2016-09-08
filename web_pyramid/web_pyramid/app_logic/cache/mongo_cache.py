from pymongo import MongoClient
import hashlib


class MongoCache:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.crawler_db
        self._collected = self._db.collected

    def get_hash_from_params(self, sources, offer_type, estate_type, city, voivodeship, similarity_threshold,
                             room_difference, size_difference, price_difference):
        hashed_str = ''.join(sources) + str(similarity_threshold) + offer_type + str(room_difference) + str(city) + \
            str(size_difference) + estate_type + str(price_difference) + str(voivodeship)

        hashed = hashlib.new('sha224')
        hashed.update(hashed_str)
        return hashed.hexdigest()

    def save_collection(self, attributes_list, url_list, hash):
        self._collected.insert_one({'key': hash, 'att': attributes_list, 'url': url_list})
