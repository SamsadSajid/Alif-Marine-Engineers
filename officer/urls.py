
from django.conf.urls import url
from django.views import generic
import officer.views as officer_views

app_name = 'officer'

urlpatterns = [
    # url(r'^dash/$', generic.FormView.as_view(
    #     form_class=form.RegistrationForm, template_name="dashboard/create_account.html")),

    url(r'^profile', officer_views.profile, name='profile'),
    url(r'^contact', officer_views.contact, name='contact'),
    url(r'^picture', officer_views.picture, name='picture'),
    url(r'^password', officer_views.password, name='password'),

    url(r'^create_account', officer_views.create_account, name='create_account'),
    url(r'^delete_account', officer_views.delete_account, name='delete_account'),
    url(r'^reset_account_pass', officer_views.reset_account_pass, name='reset_account_pass'),

    url(r'^new_order', officer_views.new_order, name='new_order'),
    url(r'^order_list', officer_views.order_list, name='order_list'),

    url(r'^add_product', officer_views.add_product, name='add_product'),
    url(r'^all_products', officer_views.all_products, name='all_products'),
    url(r'^(?P<slug>[\w-]+)/detail/', officer_views.product_details, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/', officer_views.product_edit, name='edit'),

    url(r'^logout', officer_views.logout_view, name='logout'),
]
