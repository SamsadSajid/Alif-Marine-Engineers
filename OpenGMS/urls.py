"""preseason3_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views import generic

from core import views as core_views
from authentication import views as client_auth_views
from client import views as client_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^login', core_views.login_view, name='login'),

    url(r'^signup/$', client_auth_views.signup, name='signup'),
    url(r'^account_activation_sent/$', client_auth_views.account_activation_sent,
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        client_auth_views.activate, name='activate'),
    url(r'^/pass?=success/', client_auth_views.regSuccess, name='/pass?=success/'),

    # url(r'^all_products/$', core_views.allproducts, name='all_products'),

    url(r'^auth/', include('authentication.urls')),
    url(r'^officer/', include('officer.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^production/', include('production.urls')),
    url(r'^service/', include('service.urls')),

    # products url
    url(r'^products', client_views.products, name='products'),
    url(r'^(?P<slug>[\w-]+)/detail/', client_views.product_details, name='detail'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^(?P<pk>[0-9]+)/review', client_views.review, name='review'),


    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
