import json
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crypto.crypto_message import encrypt, decrypt
from forum.models import Question

logger = logging.getLogger('django')


def create_user(username=None, first_name=None):
    return User.objects.create_user(first_name=first_name or 'Bob', last_name='Bobski',
                                    username=username or 'bob', password='123123')


def create_question(subject_text=None, question_text=None, user=None):
    if user is None:
        try:
            user = User.objects.get(username='bob')
            user.set_password('123123')
        except User.DoesNotExist:
            user = create_user()

    return Question.objects.create(
        subject=subject_text or 'Test subject',
        body=encrypt(question_text or 'Test text', key=settings.TEXT_SECRET_CODE),
        status=Question.PUBLIC,
        user=user
    )


class QuestionListingApiTests(TestCase):
    def test_authenticated_user_fetch_questions(self):
        """
        Make sure authenticated user can get question list.
        """
        create_question('Subject', 'Message')
        self.client.login(username='bob', password='123123')
        response = self.client.get(reverse('question_api'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        data = json.loads(response.content)
        for d in data:
            d.pop('id')
        self.assertEqual(data,
                         [{'subject': 'Subject', 'body': 'Message',
                           'user__first_name': 'Bob', 'user__last_name': 'Bobski'}])

    def test_not_authenticated_user_fetch_questions(self):
        """
        Make sure not authenticated user can not get question list.
        """
        create_question('Subject', 'Message')
        response = self.client.get(reverse('question_api'))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'message': 'User must be authenticated'})


class QuestionDetailApiTests(TestCase):
    def test_authenticated_user_fetch_question(self):
        """
        Make sure authenticated user can get question.
        """
        question = create_question('Subject', 'Message')
        self.client.login(username='bob', password='123123')
        response = self.client.get(reverse('question_api_detail', kwargs={'id': question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        data = json.loads(response.content)
        data.pop('id', None)
        self.assertEqual(data,
                         {'subject': 'Subject',
                          'body': 'Message',
                          'user__first_name': 'Bob', 'user__last_name': 'Bobski',
                          'answers': []})

    def test_not_authenticated_user_fetch_question(self):
        """
        Make sure not authenticated user can't get question.
        """
        question = create_question('Subject', 'Message')
        response = self.client.get(reverse('question_api_detail', kwargs={'id': question.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'message': 'User must be authenticated'})


class CreatedQuestionApiTests(TestCase):
    def test_authenticated_user_create_question(self):
        """
        Make sure authenticated user can create question.
        """
        user = create_user()
        self.client.login(username='bob', password='123123')
        response = self.client.post(reverse('question_api'),
                                    content_type='application/json',
                                    data={'subject': 'Subject',
                                          'body': 'Message'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        data = json.loads(response.content)
        data.pop('id', None)
        self.assertEqual(data,
                         {'subject': 'Subject',
                          'body': 'Message',
                          'user__first_name': 'Bob', 'user__last_name': 'Bobski',
                          'answers': []})

    def test_not_authenticated_user_create_question(self):
        """
        Make sure not authenticated user can't create question.
        """
        user = create_user()
        response = self.client.post(reverse('question_api'))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'message': 'User must be authenticated'})


class CreatedAnswerApiTests(TestCase):
    def test_authenticated_user_create_answer(self):
        """
        Make sure authenticated user can create question.
        """
        question = create_question()
        user = create_user(username='meg', first_name='Meg')
        self.client.login(username='meg', password='123123')
        response = self.client.post(reverse('answer_api'),
                                    content_type='application/json',
                                    data={'question_id': question.id,
                                          'body': 'Message'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'body': 'Message',
                          'user__first_name': 'Meg', 'user__last_name': 'Bobski'})

    def test_not_authenticated_user_create_answer(self):
        """
        Make sure not authenticated user can't create question.
        """
        question = create_question()
        user = create_user(username='rob')
        response = self.client.post(reverse('answer_api'),
                                    content_type='application/json',
                                    data={'question_id': question.id,
                                          'body': 'Message'})
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'message': 'User must be authenticated'})
