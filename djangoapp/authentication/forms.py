from django import forms
from django.forms import fields


class LoginForm(forms.Form):
    username = fields.CharField(max_length=124)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password'].widget.attrs['class'] = 'form-input'


class SignupForm(forms.Form):
    username = fields.CharField(max_length=124)
    password = fields.CharField(max_length=5)
    secret_verification_code = fields.CharField(max_length=124)
    first_name = fields.CharField()
    last_name = fields.CharField()

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password'].widget.attrs['class'] = 'form-input'
        self.fields['secret_verification_code'].widget.attrs['class'] = 'form-input'
        self.fields['first_name'].widget.attrs['class'] = 'form-input'
        self.fields['last_name'].widget.attrs['class'] = 'form-input'
