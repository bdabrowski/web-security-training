import base64
from django.conf import settings
from django.conf.urls import url

from .factory import build_router


def get_route():
    return base64.b64decode(settings.EXPON).decode('utf-8')


def router():
    return [url(get_route(), build_router())]

