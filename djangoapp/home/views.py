import json

from django.http import HttpResponseForbidden
from django.shortcuts import render


def home_view(request):
    """
    Home page of the forum.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')
    return render(request, 'home/home.html', {'first_name': request.user.first_name})
