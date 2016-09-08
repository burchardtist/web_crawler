from pyramid.view import view_config
from .wrapper import wrap


@view_config(route_name='home', renderer='templates/index.jinja2')
def home_view(request):

    return {'project': 'web_pyramid'}
