import time
import re

from datetime import timedelta

from tornado import httpclient, gen, queues, locks, ioloop

from .link_fetcher import LinkFetcher
from .links_params import links, cast_params


class HtmlFetcher:
    def __init__(self, concurrency=10):
        self._url_list = []
        self._html_list = []
        self._concurrency = concurrency

    @gen.coroutine
    def get_html(self, url):
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url)

            html = response.body if isinstance(response.body, str) else response.body.decode()
        except Exception as e:
            print('Exception: %s %s' % (e, url))
            raise gen.Return([])

        raise gen.Return(html)

    def get_links(self, sources, offer_type, estate_type, city=None, voivodeship=None):
        self._url_list = []
        self._html_list = []

        for source in sources:
            link_fetch = LinkFetcher(links[source]['start_url'], links[source]['base_url'],
                                     links[source]['offer_pattern'], links[source]['page_pattern'],
                                     cast_params(source, estate_type, offer_type, city, voivodeship))
            link_fetch.process()
            self._url_list += link_fetch.get_collected_links()

        return len(self._url_list)

    def get_all_documents(self):
        return self._html_list

    def load_all_documents(self, url_list=None):
        if url_list is not None:
            self._url_list = url_list

        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._get_all_documents)

    @gen.coroutine
    def _get_all_documents(self):
        q = queues.Queue()
        html_list = []
        collection_lock = locks.Semaphore()

        @gen.coroutine
        def fetch_url():
            current_url = yield q.get()
            try:
                html = yield self.get_html(current_url)

                collection_lock.acquire()
                html_list.append({'url': current_url, 'html': html})  # possible asynchronous access to synchronous object
                collection_lock.release()
            finally:
                q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        @gen.coroutine
        def feeder():
            for url in self._url_list:
                q.put(url)

        # Start workers, then wait for the work queue to be empty.
        feeder()
        for _ in range(self._concurrency if not re.search('gratka', self._url_list[0]) else 3):
            worker()

        yield q.join(timeout=timedelta(seconds=300))

        self._html_list = html_list

    def get_documents(self):
        sync_client = httpclient.HTTPClient()

        for url in self._url_list:
            response = sync_client.fetch(url)
            yield response.body if isinstance(response.body, str) else response.body.decode()


if __name__ == '__main__':
    hc = HtmlFetcher()
    print(hc.get_links(['olx'], 'rent', 'domy', 'Poznan', 'wielkopolskie'))  # , 'gratka', 'gumtree', 'otodom'

    a = 0

    hc.load_all_documents()
    print(len(hc.get_all_documents()))
    print(hc.get_all_documents()[:2])
