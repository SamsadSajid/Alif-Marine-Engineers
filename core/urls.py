from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views import generic

from core import views as core_views

app_name = 'core'

urlpatterns = [
    # url(r'^$', core_views.home, name='home'),
    # url(r'^login', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
]