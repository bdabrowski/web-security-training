import logging
import json
import socket

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm

logger = logging.getLogger('django')


def legacy_audit(message):
    """
    One of your very old servers we still require to send them information about each login and signup activity.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('legacyauditserver', 4001))
        sock.send(message.encode('utf-8'))
        sock.close()
    except socket.gaierror:
        logger.info('legacyauditserver is down restart docker-compose up && docker-compose down')
        return


def is_session_active(request):
    """
    API endpoint that tells if user has active session.
    """
    user_id = request.user.id if request.user.is_authenticated else None
    return HttpResponse(json.dumps({'success': request.user.is_authenticated, 'user_id': user_id}),
                        content_type='application/json')


def logout_api(request):
    """
    Ends current session.
    """
    logout(request)
    return HttpResponse(json.dumps({'success': True}),
                        content_type='application/json')


def login_view(request):
    """
    Shows login page and logs user.
    """
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(request,
                                username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                logger.info('Audit: Login successful {}'.format(form.cleaned_data))
                return redirect('home')
            else:
                logger.info('Audit: Login unsuccessful {}'.format(form.cleaned_data))
                form.add_error(field=None, error='Username or password invalid')

        context['form'] = form
        legacy_audit('User {} attempt logging unsuccessful'.format(form.cleaned_data.get('username')))
    else:
        context['form'] = LoginForm()

    return render(request, 'auth/login.html', context)


def signup_view(request):
    """
    Shows signup page and signups users.
    """
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Make sure it is someone from government and knows the password
            if form.cleaned_data.get('secret_verification_code') != settings.SIGNUP_CODE:
                logger.info('Audit: Login unsuccessful {}'.format(form.cleaned_data))
                form.add_error(field=None, error='Username or password invalid')
                context['form'] = form
                return render(request, 'auth/signup.html', context)

            User.objects.create_superuser(
                email='',
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'))
            user = authenticate(request,
                                username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            logging.info('Audit: Signup successful {}'.format(form.cleaned_data))
            return redirect('home')
        logging.info('Audit: Signup unsuccessful {}'.format(form.cleaned_data))
        legacy_audit('User {} attempt signup  unsuccessful'.format(form.cleaned_data.get('username')))
        context['form'] = form
    else:
        context['form'] = SignupForm()

    return render(request, 'auth/signup.html', context)


def intro_view(request):
    """
    Show information about the workshop.
    """
    return render(request, 'auth/workshop/intro.html', {})


def leads_view(request):
    """
    Show information about leads of existing vulnerabilities.
    """
    return render(request, 'auth/workshop/leads.html', {})


def acceptance_criteria_view(request):
    """
    Show information about acceptance criteria for this workshop.
    """
    return render(request, 'auth/workshop/acceptance_criteria.html', {})


def about_the_project(request):
    """
    Show information about acceptance criteria for this workshop.
    """
    return render(request, 'auth/workshop/acceptance_criteria.html', {})