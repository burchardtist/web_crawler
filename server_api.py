from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)


def check_documents(request):
    city = request.params.get('city', None)
    voivodeship = request.params.get('voivodeship', None)
    offer_type = request.params.get('offer_type', 'rent')
    estate_type = request.params.get('estate_type', 'mieszkania')


    if offer_type not in ['rent', 'sell', 'all'] or estate_type not in ['mieszkania', 'domy'] or (city is None and voivodeship is None):
        return Response('Bad request')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()