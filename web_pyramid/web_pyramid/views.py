from pyramid.view import view_config
from .wrapper import wrap
import json


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    sources = ['olx', 'gumtree', 'otodom', 'gratka']
    offer_type = ['rent', 'sell']
    estate_type = ['domy', 'mieszkania']

    return {
        'sources': sources,
        'offer_type': offer_type,
        'estate_type': estate_type
    }


@view_config(route_name='fetcher', renderer='templates/fetcher.jinja2')
def fetcher_view(request):
    required_params = [
        'sources',
        'offer_type',
        'estate_type'
    ]
    if request.GET:
        params = {
            'sources': request.GET.getall('sources'),
            'offer_type': request.GET['offer_type'],
            'estate_type': request.GET['estate_type']
        }
        num_params = {
            'similarity_threshold': 0.6,
            'room_difference': 1,
            'size_difference': 0.1,
            'price_difference': 0.1
        }
        none_params = [
            'city',
            'voivodeship'
        ]

        for param, default_value in num_params.items():
            if(request.GET.get(param, '')) != '':
                params[param] = num(request.GET.get(param))

        for param in none_params:
            if request.GET.get(param) == '':
                params[param] = None
            else:
                params[param] = request.GET.get(param)
        print(params)
        links_list = wrap(**params)

    submitted = True if 'form.submitted' in request.GET else False
    return {
        'links': links_list if submitted else json.dumps(links_list),
        'submitted': submitted
    }


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
