# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from production.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm, StatusForm
from order.models import Order, OrderItem
from django.shortcuts import render
from user_group.check_group import group_required
from django_tables2 import RequestConfig
from .models import Order_List


# Create your views here.


__FILE_TYPES = ['zip']


@login_required
@group_required('production_group')
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
    return render(request, 'production/profile.html', {'form': form})


@login_required
@group_required('production_group')
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
    return render(request, 'production/contact.html', {'form': form})


@login_required
@group_required('production_group')
def picture(request):
    user = request.user
    if request.method == 'POST':
        user.profile.profile_picture = request.FILES['picture']
        user.save()
        return render(request, 'production/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'production/picture.html')


@login_required
@group_required('production_group')
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
    return render(request, 'production/password.html', {'form': form})


@group_required('production_group')
def new_order(request):
    form = NewOrderForm()
    return render(request, 'production/new_order.html', {'form': form})


@group_required('production_group')
def order_list(request):
    user = request.user
    orders = Order.objects.all()
    # print (orders)
    return render(request, 'production/order_list.html', {'orders': orders})


@login_required
@group_required('production_group')
def order_view(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    order_item = OrderItem.objects.filter(order_id=pk)
    return render(request, 'production/order_view.html', {'order_item': order_item,
                                                          'order': order})


@login_required
@group_required('production_group')
def order_edit(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    order_item = OrderItem.objects.filter(order_id=pk)
    if request.method == 'POST':
        print ('baal')
        form = StatusForm(request.POST)
        order.delivery = request.POST['date']
        print(order.delivery)
        if form.is_valid():
            order.status = form.cleaned_data.get('status')
            print(order.status)
            order.save()
            return redirect('production:order_view', pk=pk)
    else:
        form = StatusForm()
        return render(request, 'production/order_edit.html', {'order_item': order_item,
                                                              'order': order, 'form': form})


@login_required
@group_required('production_group')
def logout_view(request):
    logout(request)
    return render(request, 'core/login.html')
