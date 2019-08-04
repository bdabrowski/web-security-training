import json
import logging

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

logger = logging.getLogger('django')


def create_user(username=None, first_name=None):
    return User.objects.create_user(first_name=first_name or 'Bob', last_name='Bobski',
                                    username=username or 'bob', password='123123')


class UserApiTests(TestCase):
    def test_authenticated_user_can_load_profile(self):
        """
        Make sure authenticated user can get own profile.
        """
        create_user('ron', 'Ron')
        self.client.login(username='ron', password='123123')
        response = self.client.get(reverse('user_api'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'first_name': 'Ron',
                          'last_name': 'Bobski'})

    def test_not_authenticated_user_fetch_questions(self):
        """
        Make sure not authenticated user can not get question list.
        """
        create_user('ron', 'Ron')
        response = self.client.get(reverse('user_api'))
        self.assertEqual(response.status_code, 403)


class UpdateUserApiTests(TestCase):
    def test_authenticated_user_can_update_profile(self):
        """
        Make sure authenticated user can update own profile.
        """
        create_user('ron', 'Ron')
        self.client.login(username='ron', password='123123')
        response = self.client.put(reverse('user_api'),
                                   content_type='application/json',
                                   data={'username': 'ron', 'first_name': 'Ronn',
                                         'last_name': 'Ronski'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        self.assertEqual(json.loads(response.content),
                         {'success': True, 'first_name': 'Ronn',
                          'last_name': 'Ronski'})
        ron = User.objects.get(username='ron')
        self.assertEqual(ron.first_name, 'Ronn')
        self.assertEqual(ron.last_name, 'Ronski')

    def test_not_authenticated_user_can_not_update_profile(self):
        """
        Make sure not authenticate users can not update profile.
        """
        create_user('ron', 'Ron')
        response = self.client.put(reverse('user_api'),
                                   content_type='application/json',
                                   data={'username': 'ron', 'first_name': 'Ronn',
                                         'last_name': 'Ronski'})
        self.assertEqual(response.status_code, 403)
        ron = User.objects.get(username='ron')
        self.assertEqual(ron.first_name, 'Ron')
        self.assertEqual(ron.last_name, 'Bobski')
