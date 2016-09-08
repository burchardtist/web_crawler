from pymongo import MongoClient
import hashlib

from datetime import datetime, timedelta


class MongoCache:
    def __init__(self, aging_time=8):
        self._client = MongoClient()
        self._db = self._client.crawler_db
        self._collected = self._db.collected

        self.aging_time = aging_time

    def get_hash_from_params(self, sources, offer_type, estate_type, city, voivodeship):
        hashed_str = ''.join(sources) + offer_type + str(city) + estate_type + str(voivodeship)

        hashed = hashlib.new('sha224')
        hashed.update(hashed_str)
        return hashed.hexdigest()

    def save_collection(self, attributes_list, url_list, param_hash):
        self._collected.insert_one({'key': param_hash, 'att': attributes_list, 'url': url_list,
                                    'saved': datetime.now()})

    def get_collection(self, param_hash):
        result = self._collected.find({'key': param_hash})

        if result.hasNext():
            result_document = result.next()

            if datetime.now() - result_document['saved'] > timedelta(hours=self.aging_time):
                self._collected.delete_many({'key': param_hash})
                return None, None
            else:
                return result_document['att'], result_document['url']
        else:
            return None, None
