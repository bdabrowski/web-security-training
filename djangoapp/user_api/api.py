import json

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, HttpResponse


def user_resource(request):
    """
    Secured User API.
    Only authenticated users.
    Don't allow suspect characters in fields
    Only owner can update user
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')

    if request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=request.user.username)

        if 'username' in data and data['username'] != request.user.username:
            return HttpResponseForbidden(json.dumps({'message': 'Only you can authenticate your profile'}),
                                         content_type='application/json')
        if 'first_name' in data:
            user.first_name = data['first_name'].replace('<', '').replace('>', '')
        if 'last_name' in data:
            user.last_name = data['last_name'].replace('<', '').replace('>', '')

        user.save()
        return HttpResponse(json.dumps({'success': True, 'first_name': data['first_name'],
                                        'last_name': data['last_name']}), content_type='application/json')

    return HttpResponse(json.dumps({'first_name': request.user.first_name,
                                    'last_name': request.user.last_name}),
                        content_type='application/json')
