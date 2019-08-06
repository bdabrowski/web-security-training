"""
RESTful API for question resource.

GET:  /api/forum/question/ - get the list of the public questions.
GET:  /api/forum/question/1/ - get the question with id number 1.
POST: /api/forum/question/ - create new question.
"""
import json
import logging
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpRequest

from crypto.crypto_message import encrypt, decrypt
from forum.models import Question

logger = logging.getLogger('django')


def question_resource(request):
    """
    Secured question API.
    Only authenticated users have access.
    Don't allow suspect characters in fields - prevent injections.
    Permission rules:
        You can create question only for your current user.
        Your question will be approved by the administrator.
        You can see only public questions.
        You can't modify answers.

    POST: /api/v1/forum/question/ - create question
    GET: /api/v1/forum/question/ - get list of questions
    """
    if request.method == 'POST':
        return create(request)
    else:
        return get_list(request)


def question_resource_detail(request, id):
    """
    Secured detail question API.
    Only authenticated users have access.
    Don't allow suspect characters in fields - prevent injections.
    Permission rules:
        You can see only public questions.

    GET: /api/v1/forum/question/123
    {"subject": "My Subject", "body": "Text of my question", "user__first_name": "Bob", "user__last_name": "Bobin"}
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')
    logger.info('Audit: User {} is accessing the question {}'.format(request.user.id, id))
    if request.method == 'GET' or Question.objects.get(id=id).status == Question.PUBLIC:
        question = Question.objects.get(id=id)
        return HttpResponse(json.dumps({'subject': question.subject,
                                        'id': question.id,
                                        'body': decrypt(question.body, settings.TEXT_SECRET_CODE),
                                        'user__first_name': question.user.first_name,
                                        'user__last_name': question.user.last_name,
                                        'answers': [{'user__first_name': answer.user.first_name,
                                                     'user__last_name': answer.user.last_name,
                                                     'body': decrypt(answer.body, settings.TEXT_SECRET_CODE)}
                                                    for answer in question.answer_set.all()]
                                        }),
                            content_type='application/json')
    else:
        return HttpResponseNotAllowed('Resource not allowed')


def get_list(request):
    """
    Get the JSON response of list of questions.
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')
    iterator = Question.objects.filter(status=Question.PUBLIC) \
        if not request.GET.get('q') else Question.search(request.GET.get('q'))

    data = [{'subject': question.subject,
             'body': decrypt(question.body, settings.TEXT_SECRET_CODE),
             'id': question.id,
             'user__first_name': question.user.first_name,
             'user__last_name': question.user.last_name,}
            for question in iterator]

    return HttpResponse(json.dumps(data), content_type='application/json')


def create(request: HttpRequest):
    """
    Create the question endpoint.

    Request content:
    {"subject": "My Subject", "body": "Text of my question", "user_id": 1}
    """
    if not request.user.is_authenticated:
        return HttpResponseForbidden(json.dumps({'message': 'User must be authenticated'}),
                                     content_type='application/json')
    data = json.loads(request.body.decode('utf-8'))
    question = Question()
    if 'subject' in data:
        question.subject = data['subject']
    if 'body' in data:
        question.body = encrypt(data['body'], settings.TEXT_SECRET_CODE)
    question.user_id = request.user.id
    question.status = Question.TO_BE_APPROVED
    question.save()
    return HttpResponse(json.dumps({'subject': question.subject,
                                    'body': decrypt(question.body, settings.TEXT_SECRET_CODE),
                                    'user__first_name': request.user.first_name,
                                    'user__last_name': request.user.last_name,
                                    'answers': [],
                                    'id': question.id}),
                        content_type='application/json')
