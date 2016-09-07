links = {'olx':
             {'base_url': 'http://olx.pl/',
              'start_url': 'http://olx.pl/nieruchomosci/{type}/{offer_type}/{city}/',
              'offer_pattern': '/oferta/',
              'page_pattern': '\?page=\d$'},
         'gratka':
             {'start_url': 'http://dom.gratka.pl/{type}-{offer_type}/lista/{city}.html',
              'base_url': 'http://dom.gratka.pl/',
              'offer_pattern': '/tresc/',
              'page_pattern': '\d+,\d+,li,s.html$'},
         'gumtree':
             {'start_url': 'http://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/{city}/{type}/{code}',
              'base_url': 'http://www.gumtree.pl',
              'offer_pattern': 'a-mieszkania-i-domy-do-wynajecia',
              'page_pattern': '/page-\d+/'},
         'otodom':
             {'start_url': 'https://otodom.pl/{offer_type}/{type}/{city}/',
              'base_url': 'https://otodom.pl/',
              'offer_pattern': '/oferta/',
              'page_pattern': '{city}/\?page=\d+$'}
         }

offer_type_dict = {'olx':
                       {'rent': 'wynajem',
                        'sell': 'sprzedaz',
                        'all': 'all'
                        },
                   'gratka':
                       {'rent': 'do-wynajecia',
                        'sell': 'sprzedam'
                        },
                   'otodom':
                       {'rent': 'wynajem',
                        'sell': 'sprzedaz'
                        }
                   }

gumtree_location_codes = {'czeladz': 'l3200547', 'podkarpackie': 'l32000', 'biala-podlaska': 'l3200137',
                          'dabrowa-gornicza': 'l3200281', 'katy-wroclawskie': 'l3200621',
                          'bukowina-tatrzanska': 'l3200202', 'libiaz': 'l3200483', 'kepno': 'l3200350',
                          'bedzin': 'l3200273', 'zawiercie': 'l3200305', 'inowroclaw': 'l3200124',
                          'pn-+-wsch-powiaty': 'l3200036', 'olesnica': 'l3200103', 'bytom': 'l3200277',
                          'slaskie': 'l3200002', 'sokolka': 'l3200269', 'wroclaw': 'l3200114', 'olawa': 'l3200102',
                          'czestochowa': 'l3200280', 'lancut': 'l3200246', 'kielce': 'l3200311',
                          'czerwionka+leszczyny': 'l3200548', 'lukow': 'l3200147', 'sieradz': 'l3200192',
                          'lodzkie': 'l3200004', 'bydgoszcz': 'l3200120', 'gdynia': 'l3200073',
                          'jelenia-gora': 'l3200092', 'tomaszow-mazowiecki': 'l3200194', 'nisko': 'l3200248',
                          'katowice': 'l3200285', 'tarnobrzeg': 'l3200256', 'biskupiec': 'l3200322',
                          'lubelskie': 'l3200076', 'pd-+-zach-powiaty': 'l3200044', 'polkowice': 'l3200105',
                          'skawina': 'l3200218', 'podlaskie': 'l3200080', 'pomorskie': 'l3200005', 'lodz': 'l3200183',
                          'pn-+-zach-powiaty': 'l3200041', 'srem': 'l3200371', 'mosina': 'l3200358',
                          'leszno': 'l3200355', 'wielkopolskie': 'l3200006', 'mszana-dolna': 'l3200484',
                          'gizycko': 'l3200328', 'opole': 'l3200234', 'swarzedz': 'l3200369', 'sosnowiec': 'l3200297',
                          'bielsko+biala': 'l3200274', 'wielun': 'l3200195', 'mazowieckie': 'l3200001',
                          'tuszyn': 'l3200476', 'kujawsko-+-pomorskie': 'l3200075', 'gdansk': 'l3200072',
                          'kolo': 'l3200351', 'ostroda': 'l3200339', 'malopolskie': 'l3200003', 'opolskie': 'l3200078',
                          'kalisz': 'l3200349', 'karpacz': 'l3200094', 'myslowice': 'l3200289', 'puck': 'l3200423',
                          'wrzesnia': 'l3200377', 'bochnia': 'l3200200', 'poznan': 'l3200366', 'olkusz': 'l3200215',
                          'klobuck': 'l3200286', 'nowy-sacz': 'l3200213', 'belzyce': 'l3200465', 'olsztyn': 'l3200338',
                          'zachodnie-powiaty': 'l3200046', 'czersk': 'l3200539', 'myslenice': 'l3200212',
                          'zdunska-wola': 'l3200197', 'oborniki': 'l3200361', 'malbork': 'l3200420',
                          'zachodniopomorskie': 'l3200084', 'bialystok': 'l3200259', 'koscielisko': 'l3200207',
                          'chelmza': 'l3200455', 'konin': 'l3200352', 'krosno': 'l3200242', 'mazury': 'l3200083',
                          'mielec': 'l3200247', 'torun': 'l3200132', 'olecko': 'l3200337', 'jaroslaw': 'l3200239',
                          'ropczyce': 'l3200251', 'czaplinek': 'l3200586', 'ostrow-wielkopolski': 'l3200362',
                          'kutno': 'l3200179', 'niepolomice': 'l3200485', 'walbrzych': 'l3200112',
                          'swietokrzyskie': 'l3200082', 'jastrzebie+zdroj': 'l3200283',
                          'gorzow-wielkopolski': 'l3200157', 'strzelin': 'l3200107', 'pabianice': 'l3200186',
                          'miastko': 'l3200538', 'nowy-targ': 'l3200214', 'zakopane': 'l3200225',
                          'olsztynek': 'l3200568', 'rabka+zdroj': 'l3200487', 'lubuskie': 'l3200077',
                          'lomza': 'l3200265', 'bardo': 'l3200595', 'dzierzoniow': 'l3200088',
                          'konstantynow-lodzki': 'l3200178', 'sroda-slaska': 'l3200108', 'suwaki': 'l3200270',
                          'wronki': 'l3200581', 'boleslawiec': 'l3200087', 'wieliczka': 'l3200224',
                          'wejherowo': 'l3200432', 'zgierz': 'l3200198', 'lublin': 'l3200145', 'wloclawek': 'l3200135',
                          'szczytno': 'l3200341', 'skoczow': 'l3200561', 'wadowice': 'l3200223', 'wolbrom': 'l3200490',
                          'radzyn-podlaski': 'l3200151', 'belchatow': 'l3200175', 'mikolow': 'l3200288',
                          'szklarska-poreba': 'l3200106', 'tychy': 'l3200301', 'legnica': 'l3200096',
                          'slupsk': 'l3200426', 'warszawa': 'l3200008', 'krzeszowice': 'l3200482', 'gubin': 'l3200159',
                          'pisz': 'l3200340', 'lubon': 'l3200356', 'cedynia': 'l3200381', 'sopot': 'l3200074',
                          'brzesko': 'l3200201', 'znin': 'l3200136', 'pruszcz-gdanski': 'l3200422',
                          'slomniki': 'l3200619', 'dolnoslaskie': 'l3200007', 'zywiec': 'l3200307',
                          'ustrzyki-dolne': 'l3200257', 'tarnowskie-gory': 'l3200300', 'gryfino': 'l3200389',
                          'lubartow': 'l3200144', 'krakow': 'l3200208', 'andrespol': 'l3200588',
                          'kazimierza-wielka': 'l3200310', 'wschodnie-powiaty': 'l3200045',
                          'stargard-szczecinski': 'l3200401', 'polnocne-powiaty': 'l3200027', 'drezdenko': 'l3200158',
                          'cieszyn': 'l3200279', 'tarnow': 'l3200221', 'zielona-gora': 'l3200171',
                          'pd-+-wsch-powiaty': 'l3200043', 'zgorzelec': 'l3200116', 'sycow': 'l3200450',
                          'slupca': 'l3200368', 'przemysl': 'l3200249', 'szczecin': 'l3200402', 'swidnica': 'l3200109',
                          'rzeszow': 'l3200252', 'walcz': 'l3200406', 'gryfow-slaski': 'l3200442', 'tczew': 'l3200430',
                          'zabrze': 'l3200304', 'lask': 'l3200180', 'trzebnica': 'l3200111',
                          'poludniowe-powiaty': 'l3200042'}


def cast_params(page, estate_type, offer_type, city, voivodeship):
    try:
        if page == 'olx':
            return {'type': estate_type, 'offer_type': offer_type_dict[page][offer_type],
                    'city': city if city is not None else voivodeship}
        elif page == 'gratka':
            return {'type': estate_type, 'offer_type': offer_type_dict[page][offer_type],
                    'city': '{},{}'.format(voivodeship, city).lower()}
        elif page == 'gumtree':
            return {'type': 'mieszkanie' if estate_type == 'mieszkania' else 'dom', 'city': city,
                    'code': gumtree_code_generator(voivodeship, city)}
        elif page == 'otodom':
            return {'type': 'mieszkanie' if estate_type == 'mieszkania' else 'dom',
                    'city': city if city is not None else voivodeship,
                    'offer_type': offer_type_dict[page][offer_type]}
        else:
            raise ValueError("Unknown webpage.")
    except KeyError:
        raise ValueError("Given offer type not supported for chosen webpage.")


def gumtree_code_generator(voivodeship, city):
    basic = 'v1c9008a1dwp1'

    if city is None:
        return basic[:7] + gumtree_location_codes[voivodeship.lower()] + basic[-6:]
    else:
        return basic[:7] + gumtree_location_codes[city.lower()] + basic[-6:]
