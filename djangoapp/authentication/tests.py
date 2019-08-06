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


class SignupViewTest(TestCase):
    def test_valid_signup(self):
        """
        Make sure users can signup.
        """
        signup_data = {
            'username': 'bob',
            'password': '123123',
            'secret_verification_code': settings.SIGNUP_CODE,
            'first_name': 'Bob',
            'last_name': 'Bobski'
        }
        response = self.client.post(reverse('auth_signup'), data=signup_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_invalid_signup(self):
        """
        Make sure invalid signup attempts are rejected.
        """
        signup_data = {
            'username': 'bob',
            'password': '',
            'secret_verification_code': settings.SIGNUP_CODE,
            'first_name': 'Bob',
            'last_name': 'Bobski'
        }
        response = self.client.post(reverse('auth_signup'), data=signup_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')


class LoginViewTests(TestCase):

    def test_user_login(self):
        """
        Make sure users can login.
        """
        create_user()
        data = {
            'username': 'bob',
            'password': '123123',
        }
        response = self.client.post(reverse('auth_login') + '/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_not_authenticated_user_fetch_question(self):
        """
        Make sure invalid login attempts are rejected.
        """
        question = create_question('Subject', 'Message')
        response = self.client.get(reverse('question_api_detail', kwargs={'id': question.id}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'message': 'User must be authenticated'})

