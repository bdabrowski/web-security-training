from django import forms
from django.forms import fields


class LoginForm(forms.Form):
    username = fields.CharField(max_length=124)
    password = fields.CharField(max_length=124)


class SignupForm(forms.Form):
    username = fields.CharField(max_length=124)
    password = fields.CharField(max_length=5)
    secret_verification_code = fields.CharField(max_length=124)
    first_name = fields.CharField()
    last_name = fields.CharField()
