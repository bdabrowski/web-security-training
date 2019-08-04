from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from faker import Faker

from crypto.crypto_message import encrypt
from forum.models import Question, Answer


def create_user(username=None, first_name=None, last_name=None):
    return User.objects.create_user(first_name=first_name or 'Bob', last_name=last_name or 'Bobski',
                                    username=username or 'bob', password='123123')


def create_rob():
    return create_user(username='rob', first_name='Rob')


def create_random_user():
    fake = Faker()
    profile = fake.profile()
    try:
        return User.objects.get(username=profile['username'], first_name=fake.first_name(),
                                last_name=fake.last_name())
    except User.DoesNotExist:
        return create_user(username=profile['username'], first_name=fake.first_name(),
                           last_name=fake.last_name())


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        questions = [
            {'subject': 'How to improve voting ratings',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'Intelligence information about our country',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'Here we put ideas how to improve economy',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'How to reduce plastic production',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'Information about trade war',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'How to use internet for voting',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
            {'subject': 'How crypto currency will impact our national bank ratings',
             'body': encrypt(fake.text(), settings.TEXT_SECRET_CODE)},
        ]

        for question in questions:
            Question.objects.create(subject=question['subject'], body=question['body'], user=create_random_user())

        try:
            rob = User.objects.get(username='rob')
        except User.DoesNotExist:
            rob = create_rob()

        answers = [
            {'body': fake.text()},
            {'body': fake.text()},
            {'body': fake.text()},
            {'body': fake.text()},
            {'body': fake.text()},
            {'body': fake.text()},
            {'body': fake.text()},
        ]

        for answer in answers:
            Answer.objects.create(question=Question.objects.all().order_by('?').first(),
                                  body=answer['body'], user=create_random_user())
