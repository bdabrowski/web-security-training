"""
RESTful API for question resource.

GET: /api/v1/question/ - get the list of the public questions.
GET: /api/v1/question/1/ - get the question with id number 1.
POST: /api/v1/question/ - create new question.
"""

import json

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed

from crypto.crypto_message import encrypt, decrypt
from forum.models import Question, Answer


def answer_resource(request):
    """
    Secured answer API.
    Only authenticated users have access.
    Don't allow suspect characters in fields - prevent injections.
    Permission rules:
        You can create answer only for your current user.
        Your question will be approved by the administrator.
        You can see only public questions.
        You can't modify answers.

    POST: /api/v1/forum/question/ - create question
    GET: /api/v1/forum/question/ - get list of questions
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')
    if request.method != 'POST':
        return HttpResponseNotAllowed('Method not allowed')
    data = json.loads(request.body.decode('utf-8'))
    answer = Answer()
    if 'question_id' not in data:
        return HttpResponseForbidden(json.dumps({'message': 'The question_id is required'}),
                                     content_type='application/json')
    if 'body' in data:
        answer.body = encrypt(data['body'], settings.TEXT_SECRET_CODE)
    answer.user_id = request.user.id
    answer.question_id = data['question_id']
    answer.save()
    return HttpResponse(json.dumps({'body': decrypt(answer.body, settings.TEXT_SECRET_CODE),
                                    'question_id': answer.question_id,
                                    'user__first_name': answer.user.first_name,
                                    'user__last_name': answer.user.last_name}),
                        content_type='application/json')
