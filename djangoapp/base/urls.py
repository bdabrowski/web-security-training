from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url

from user_api.api import user_resource
from .utils.router.core import router
from authentication.views import login_view, signup_view, is_session_active, logout_api, intro_view, leads_view, \
    acceptance_criteria_view, about_the_project
from home.views import home_view
from forum_api.answer import answer_resource
from forum_api.question import question_resource_detail, question_resource

urlpatterns = [
    url('^$', home_view, name='home'),
    url('^admin/', admin.site.urls),
    url('^auth/login', login_view, name='auth_login'),
    url('^auth/signup', signup_view, name='auth_signup'),
url('^auth/intro', intro_view),
url('^auth/leads', leads_view),
url('^auth/ac', acceptance_criteria_view),
url('^auth/about', about_the_project),
    url('^api/v1/auth/session', is_session_active, name='auth_session'),
    url('^api/v1/auth/logout', logout_api, name='auth_logout'),
    url('^api/v1/forum/profile/', user_resource, name='user_api'),
    url('^api/v1/forum/question/$', question_resource, name='question_api'),  # GET list or POST new question
    url('^api/v1/forum/question/(?P<id>[-\w\d]+)/', question_resource_detail, name='question_api_detail'),  # GET one question
    url('^api/v1/forum/answer/$', answer_resource, name='answer_api'),  # POST new answer

] + static(settings.MEDIA_DEV_URL, document_root=settings.MEDIA_ROOT) + router()


