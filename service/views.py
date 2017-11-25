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
from service.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm
from django.shortcuts import render
from user_group.check_group import group_required
from django_tables2 import RequestConfig
from .models import Order_List


# Create your views here.


__FILE_TYPES = ['zip']


@login_required
@group_required('service_group')
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.sex = form.cleaned_data.get('sex')
            user.email = form.cleaned_data.get('email')
            user.profile.about = form.cleaned_data.get('about')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileForm(instance=user, initial={
            'sex': user.profile.sex,
            'about': user.profile.about,
            })
    return render(request, 'service/profile.html', {'form': form})


@login_required
@group_required('service_group')
def contact(request):
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user.profile.address = form.cleaned_data.get('address')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.state = form.cleaned_data.get('state')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.zip = form.cleaned_data.get('zip')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your contact was successfully edited.')

    else:
        form = ContactForm(instance=user, initial={
            'address': user.profile.address,
            'city': user.profile.city,
            'state': user.profile.state,
            'country': user.profile.country,
            'phone': user.profile.phone,
            'zip': user.profile.zip,
        })
    return render(request, 'service/contact.html', {'form': form})


@login_required
@group_required('service_group')
def picture(request):
    user = request.user
    if request.method == 'POST':
        user.profile.profile_picture = request.FILES['picture']
        user.save()
        return render(request, 'service/picture.html')
    print (user.profile.profile_picture)
    return render(request, 'service/picture.html')


@login_required
@group_required('service_group')
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


def create_account(request):
    return render(request, 'service/create_account.html')


def delete_account(request):
    return render(request, 'service/delete_account.html')


def reset_account_pass(request):
    return render(request, 'service/reset_account_pass.html')


@group_required('service_group')
def select_manager(request):
    return render(request, 'service/select_manager.html')


@group_required('service_group')
def new_order(request):
    form = NewOrderForm()
    return render(request, 'service/new_order.html', {'form': form})


@group_required('service_group')
def order_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    return render(request, 'service/order_list.html')


@login_required
@group_required('service_group')
def logout_view(request):
    logout(request)
    return render(request, 'core/login.html')