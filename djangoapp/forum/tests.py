from django.contrib.auth.models import User
from django.test import TestCase

from forum.models import Question


class QuestionTestCase(TestCase):

    def test_search(self):
        user = User.objects.create(username='test', email='test@example.com')
        Question.objects.create(subject='test', body='test', user=user)
        Question.objects.create(subject='egg test', body='egg test', user=user)
        Question.objects.create(subject='test spam', body='test spam', user=user)
        Question.objects.create(subject='spam egg', body='spam egg', user=user)

        query_test = Question.search('test')
        self.assertEqual(query_test.count(), 3)

        query_test = Question.search('egg')
        self.assertEqual(query_test.count(), 2)

        query_test = Question.search('spam')
        self.assertEqual(query_test.count(), 2)
