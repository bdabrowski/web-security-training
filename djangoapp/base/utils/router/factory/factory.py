from django.http import Http404


def build_router():
    return ['/core/', Http404]

