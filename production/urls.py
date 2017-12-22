from django.conf.urls import url
from django.views import generic
import production.views as production_views

app_name = 'production'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', production_views.profile, name='profile'),
    url(r'^contact', production_views.contact, name='contact'),
    url(r'^picture', production_views.picture, name='picture'),
    url(r'^password', production_views.password, name='password'),

    url(r'^new_order', production_views.new_order, name='new_order'),
    url(r'^order_list', production_views.order_list, name='order_list'),

    url(r'^(?P<pk>[0-9]+)/order_view', production_views.order_view, name='order_view'),
    url(r'^(?P<pk>[0-9]+)/order_edit', production_views.order_edit, name='order_edit'),

    url(r'^notification', production_views.notification, name='notification'),

    url(r'^logout', production_views.logout_view, name='logout'),
]
