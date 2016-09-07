links = {'olx':
             {'base_url': 'http://olx.pl/',
              'start_url': 'http://olx.pl/nieruchomosci/{type}/{offer_type}/{city}/',
              'offer_pattern': '/oferta/',
              'page_pattern': '\?page=\d$'},
         'gratka':
             {'start_url': 'http://dom.gratka.pl/{type}-{offer_type}/lista/{city}.html',
              'base_url': 'http://dom.gratka.pl/',
              'offer_pattern': '/tresc/',
              'page_pattern': '\d+,\d+,li,s.html$'}
         }

offer_type_dict = {'olx':
                       {'rent': 'wynajem',
                        'sell': 'sprzedaz',
                        'all': 'all'
                        },
                   'gratka':
                       {'rent': 'do-wynajecia',
                        'sell': 'sprzedam'
                        }
                   }


def cast_params(page, type, offer_type, city, voivodeship):
    if page == 'olx':
        return {'type': type, 'offer_type': offer_type_dict[page][offer_type], 'city': city}
    elif page == 'gratka':
        return {'type': type, 'offer_type': offer_type_dict[page][offer_type],
                'city': '{},{}'.format(voivodeship, city).lower()}
