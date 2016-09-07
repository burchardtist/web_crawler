import time
import re
from datetime import timedelta
from crawler.links_params import links

try:
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urldefrag
except ImportError:
    from html.parser import HTMLParser
    from urllib.parse import urljoin, urldefrag

from tornado import httpclient, gen, ioloop, queues, locks


class LinkFetcher:
    def __init__(self, base_fetch_url, base_url, offer_pattern, page_pattern, params, concurrency=4):
        self._base_fetch_url = base_fetch_url.format(**params)

        if params['offer_type'] == 'all':
            self._base_fetch_url = self._base_fetch_url.replace('/all', '')

        self._base_url = base_url

        self._offer_pattern = offer_pattern
        self._page_pattern = page_pattern

        self._links = []
        self._concurrency = concurrency

    def get_collected_links(self):
        return self._links

    @gen.coroutine
    def get_links_from_url(self, url):
        """Download the page at `url` and parse it for links.

        Returned links have had the fragment after `#` removed, and have been made
        absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes
        'http://www.tornadoweb.org/en/stable/gen.html'.
        """
        try:
            response = yield httpclient.AsyncHTTPClient().fetch(url)
            print('fetched %s' % url)

            html = response.body if isinstance(response.body, str) \
                else response.body.decode()
            urls = [urljoin(url, self.remove_fragment(new_url))
                    for new_url in self.get_links(html)]
        except Exception as e:
            print('Exception: %s %s' % (e, url))
            raise gen.Return([])

        raise gen.Return(urls)

    def remove_fragment(self, url):
        pure_url, frag = urldefrag(url)
        return pure_url

    def get_links(self, html):
        class URLSeeker(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.urls = []

            def handle_starttag(self, tag, attrs):
                href = dict(attrs).get('href')
                if href and tag == 'a':
                    self.urls.append(href)

        url_seeker = URLSeeker()
        url_seeker.feed(html)
        return url_seeker.urls

    def process(self):
        io_loop = ioloop.IOLoop.current()
        io_loop.run_sync(self._process)

    @gen.coroutine
    def _process(self):
        q = queues.Queue()
        start = time.time()
        fetching, fetched, collection = set(), set(), set()
        collection_lock = locks.Semaphore()

        @gen.coroutine
        def fetch_url():
            current_url = yield q.get()
            try:
                if current_url in fetching:
                    return

                print('fetching %s' % current_url)
                fetching.add(current_url)
                urls = yield self.get_links_from_url(current_url)
                fetched.add(current_url)

                for new_url in urls:
                    # Only follow links beneath the base URL and next pages, remember offers
                    if re.search(self._offer_pattern, new_url) and re.match(self._base_url, new_url):
                        collection_lock.acquire()
                        collection.add(new_url)  # possible asynchronous access to synchronous object
                        collection_lock.release()
                    elif re.search(self._page_pattern, new_url) and re.match(self._base_fetch_url, new_url):
                        yield q.put(new_url)

            finally:
                q.task_done()

        @gen.coroutine
        def worker():
            while True:
                yield fetch_url()

        q.put(self._base_fetch_url)

        # Start workers, then wait for the work queue to be empty.
        for _ in range(self._concurrency):
            worker()
        yield q.join(timeout=timedelta(seconds=300))
        assert fetching == fetched
        print('Done in %d seconds, fetched %s URLs.' % (
            time.time() - start, len(fetched)))

        self._links = list(collection)

if __name__ == '__main__':
    l_f = LinkFetcher(links['olx']['start_url'], links['olx']['base_url'], links['olx']['offer_pattern'],
                      links['olx']['page_pattern'], {'city': 'poznan', 'type': 'domy', 'offer_type': 'wynajem'})

    l_f.process()
    print(l_f.get_collected_links())
