from pyramid.view import view_config
from .wrapper import test


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):
    test()
    return {'project': 'web_pyramid'}
