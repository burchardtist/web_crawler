from ..app_logic.crawler.link_fetcher import LinkFetcher
from ..app_logic.crawler.links_params import links, cast_params


def test():
    params = {'city': 'poznan', 'estate_type': 'domy', 'offer_type': 'rent', 'voivodeship': 'wielkopolskie'}
    all_links = {}

    for page in ['olx', 'gratka', 'gumtree', 'otodom']:
        l_f = LinkFetcher(links[page]['start_url'], links[page]['base_url'], links[page]['offer_pattern'],
                          links[page]['page_pattern'], cast_params(page, **params), verbose=0)

        l_f.process()
        all_links[page] = l_f.get_collected_links()
        print(len(all_links))

    print(all_links[0])
    print(all_links[-1])

if __name__ == '__main__':
    test()
