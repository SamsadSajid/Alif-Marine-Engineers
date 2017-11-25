# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from client.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm
from officer.models import ProductList, ProductReview
from star_ratings.models import Rating
from cart.forms import CartAddProductForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from order.models import Order, OrderItem
from user_group.check_group import group_required
from django.contrib.auth import logout
# from .tables import OrderTable

__FILE_TYPES = ['zip']


@login_required(login_url='/login/')
@group_required('client_group')
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            # user.birth_date = form.cleaned_data.get('birth_date')
            # user.profile.job_title = form.cleaned_data.get('job_title')  # profile is for user profile
            user.profile.sex = form.cleaned_data.get('sex')
            user.email = form.cleaned_data.get('email')
            # user.profile.url = form.cleaned_data.get('url')
            # user.profile.location = form.cleaned_data.get('location')
            user.profile.about = form.cleaned_data.get('about')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        # form = ProfileForm(instance=user, initial={
        #     'job_title': user.profile.job_title,
        #     'url': user.profile.url,
        #     'location': user.profile.location
        #     })
        form = ProfileForm(instance=user, initial={
            'sex': user.profile.sex,
            'about': user.profile.about,
        })
    return render(request, 'client/client_profile.html', {'form': form})


@login_required(login_url='/login/')
@group_required('client_group')
def contact(request):
    user = request.user
    if request.method == 'POST':
        # form = ContactForm()
        form = ContactForm(request.POST)
        if form.is_valid():
            user.profile.address = form.cleaned_data.get('address')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.zip = form.cleaned_data.get('zip')

            # user.birth_date = form.cleaned_data.get('birth_date')
            # user.profile.job_title = form.cleaned_data.get('job_title')  # profile is for user profile
            # user.sex = form.cleaned_data.get('sex')
            # user.email = form.cleaned_data.get('email')
            # user.profile.url = form.cleaned_data.get('url')
            # user.profile.location = form.cleaned_data.get('location')
            # user.profile.about = form.cleaned_data.get('about')

            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your contact was successfully edited.')

    else:
        # form = ProfileForm(instance=user, initial={
        #     'job_title': user.profile.job_title,
        #     'url': user.profile.url,
        #     'location': user.profile.location
        #     })
        form = ContactForm(instance=user, initial={
            'address': user.profile.address,
            'city': user.profile.city,
            'state': user.profile.state,
            'country': user.profile.country,
            'phone': user.profile.phone,
            'zip': user.profile.zip,
        })
    return render(request, 'client/client_contact.html', {'form': form})


@login_required(login_url='/login/')
@group_required('client_group')
def picture(request):
    user = request.user
    if request.method == 'POST':
        user.profile.profile_picture = request.FILES['picture']
        user.save()
        return render(request, 'client/client_picture.html')
    print (user.profile.profile_picture)
    return render(request, 'client/client_picture.html')


@login_required(login_url='/login/')
@group_required('client_group')
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect('password/')

    else:
        form = ChangePasswordForm(instance=user)
    # form = ChangePasswordForm()
    return render(request, 'client/client_password.html', {'form': form})


# def create_account(request):
#     return render(request, 'dashboard/create_account.html')
#
#
# def delete_account(request):
#     return render(request, 'dashboard/delete_account.html')
#
#
# def reset_account_pass(request):
#     return render(request, 'dashboard/reset_account_pass.html')

@login_required(login_url='/login/')
@group_required('client_group')
def new_order(request):
    form = NewOrderForm()
    return render(request, 'client/client_new_order.html', {'form': form})


@login_required(login_url='/login/')
def order_list(request):
    user = request.user
    orders = Order.objects.filter(email=user.email)
    print (orders)
    return render(request, 'client/order_list.html', {'orders': orders})


@login_required(login_url='/login/')
@group_required('client_group')
def order_view(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    order_item = OrderItem.objects.filter(order_id=pk)
    return render(request, 'client/order_view.html', {'order_item': order_item,
                                                      'order': order})


@login_required(login_url='/login/')
@group_required('client_group')
def order_edit(request):
    form = NewOrderForm()
    return render(request, 'client/order_edit.html', {'form': form})


# view for all products. Even if a user is not authenticated, can view this page. Can view details of the
# product. But cannot use 'add to cart' privilege!!!


def products(request):
    _products = ProductList.objects.all()
    paginator = Paginator(_products, 9)
    page = request.GET.get('page', 1)  # returns the 1st page
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    return render(request, 'client/all_products.html', {'product_list': product_list})


def product_details(request, slug):
    product = get_object_or_404(ProductList, slug=slug)
    product_review = ProductReview.objects.filter(product_id=product.product_id)
    rating_count = Rating.objects.filter(object_id=product.id)
    # print (product_review.values(review))
    cart_product_form = CartAddProductForm()
    return render(request, 'client/products_detail.html', {
        'product': product,
        'product_review': product_review,
        'rating_count': rating_count,
        'cart_product_form': cart_product_form,
    })


@group_required('client_group')
def review(request, pk):
    user = request.user
    product = get_object_or_404(ProductList, id=pk)
    # print (product)
    rating = Rating.objects.get(object_id=pk)
    # print ('rating is {}'.format(rating))
    product_review = ProductReview()
    product_review.product_id = product.product_id
    product_review.product_name = product.product_name
    # print('rating {}'.format(rating.object_id))
    product_review.rank = rating.total
    product_review.reviewed_by = user
    product_review.review = request.POST.get('comment')
    product_review.save()
    return redirect('detail', slug=product.slug)


@login_required(login_url='/login/')
@group_required('client_group')
def logout_view(request):
    logout(request)
    return render(request, 'core/login.html')