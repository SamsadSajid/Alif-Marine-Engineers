# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import os
from PIL import Image
from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from user_group.check_group import group_required
from officer.form import ProfileForm, ChangePasswordForm, ContactForm, NewOrderForm, ProductForm
from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import ProductList
from .tables import OrderTable
from django.contrib.auth import logout

# Create your views here.


__FILE_TYPES = ['zip']


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/profile.html', {'form': form})


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/contact.html', {'form': form})


@login_required
@group_required('officer_group')
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    print(uploaded_picture)
    return render(request, 'dashboard/picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
@group_required('officer_group')
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_pictures/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/picture/')


@login_required
@group_required('officer_group')
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + \
                       request.user.username + '_tmp.jpg'
        filename = django_settings.MEDIA_ROOT + '/profile_pictures/' + \
                   request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('picture/')


@login_required
@group_required('officer_group')
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
    return render(request, 'dashboard/password.html', {'form': form})


@login_required
@group_required('officer_group')
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # email = request.POST.get('email', False)
        account_type = request.POST.get('account_type')
        print (username)
        # print (email)
        print (account_type)

        account_types = {'Technical Officer': 1, 'Service Manager': 2, 'Production Manager': 3}
        if username and account_type != 'Account Type':
            if not User.objects.filter(username=username).exists():
                rand_password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                print("Generated Password " + rand_password)
                user = User.objects.create_user(username=username, password=rand_password)
                user.profile.account_type = account_types[account_type]
                user.save()
                print('user is saved')
                # NewUser(user=user, password=password).save()
                # messages.success(request, 'Created account successfully.')
                messages.add_message(request,
                                     messages.SUCCESS,
                                     "Account is created successfully!")
                return redirect('/officer/create_account')
            else:
                # messages.error(request, 'Submitted form is not valid. User already exist.')
                messages.add_message(request,
                                     messages.ERROR,
                                     "Submitted form is not valid. User already exist!")
                return redirect('/officer/create_account')

        else:
            # messages.error(request, 'Submitted form is not valid. Try again.')
            messages.add_message(request,
                                 messages.ERROR,
                                 "Submitted form is not valid! Try again.")
            return render(request, 'dashboard/create_account.html')
    else:
        return render(request, 'dashboard/create_account.html')


@group_required('officer_group')
def delete_account(request):
    return render(request, 'dashboard/delete_account.html')


@group_required('officer_group')
def reset_account_pass(request):
    return render(request, 'dashboard/reset_account_pass.html')


@group_required('officer_group')
def new_order(request):
    form = NewOrderForm()
    return render(request, 'dashboard/new_order.html', {'form': form})


@group_required('officer_group')
def order_list(request):
    # table = OrderTable(Order_List.objects.all())
    # RequestConfig(request).configure(table)
    return render(request, 'dashboard/order_list.html')


@login_required
@group_required('officer_group')
def add_product(request):
    user = request.user
    product_list = ProductList()
    if request.method == 'POST':
        print ('yoo')
        form = ProductForm(request.POST, request.FILES)
        print ('yoo')
        print (form)
        if form.is_valid():
            print ('yoo')
            product_list.product_id = form.cleaned_data.get('product_id')
            print (product_list.product_id)
            product_list.product_name = form.cleaned_data.get('product_name')
            product_list.uploaded_by = user
            product_list.quantity = form.cleaned_data.get('quantity')
            product_list.product_available = form.cleaned_data.get('product_available')
            product_list.product_description = form.cleaned_data.get('product_description')
            product_list.slug = product_list.product_name.replace(' ', '-')
            product_list.product_image = request.FILES['product_image']
            file_type = product_list.product_image.url.split('.')[-1]
            file_type = file_type.lower()
            product_list.save()

            # product = form.save(commit=False)
            # product.uploaded_by = user
            # product.product_image = request.FILES['product_image']
            # form.save()
            # return render(request, 'dashboard/all_product.html', {'form': form})
            return redirect('/officer/all_products/')
        else:
            form = ProductForm()
            print (form.errors)
            messages.add_message(request,
                                 messages.ERROR,
                                 "Submitted form is not valid! Try again.")
            return render(request, 'dashboard/add_products.html', {'form': form})
    else:
        form = ProductForm(instance=product_list, initial={
            'product_id': product_list.product_id,
            'product_name': product_list.product_name,
            'product_image': product_list.product_image,
            'quantity': product_list.quantity,
            'product_available': product_list.product_available,
            'product_description': product_list.product_description
        })
        return render(request, 'dashboard/add_products.html', {'form': form})


@login_required
@group_required('officer_group')
def all_products(request):
    user = request.user
    print (user)
    product_list = ProductList.objects.all()
    product_list_by_user = ProductList.objects.filter(uploaded_by=user)
    # nicher line gula edit kora lagbe. Editing privilege deya lagbe. Bug ache niche
    if product_list_by_user:
        print ("mnm")
        return render(request, 'dashboard/all_products.html', {'product_list': product_list, 'user': user})
    else:
        return render(request, 'dashboard/all_products.html', {'product_list': product_list})


@login_required
@group_required('officer_group')
def product_details(request, slug):
    product = get_object_or_404(ProductList, slug=slug)
    return render(request, 'dashboard/products_detail.html', {'product': product})


@login_required
@group_required('officer_group')
def product_edit(request, slug):
    product = get_object_or_404(ProductList, slug=slug)
    print (product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print ('yoo')
        if form.is_valid():
            product.product_id = form.cleaned_data.get('product_id')
            print (product.product_id)
            product.product_name = form.cleaned_data.get('product_name')
            product.quantity = form.cleaned_data.get('quantity')
            product.product_available = form.cleaned_data.get('product_available')
            product.product_description = form.cleaned_data.get('product_description')
            product.slug = product.product_name.replace(' ', '-')
            product.product_image = request.FILES['product_image']
            file_type = product.product_image.url.split('.')[-1]
            file_type = file_type.lower()
            product.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 "Product information has been edited successfully.")
            return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})
        else:
            print (form.errors)
            messages.add_message(request,
                                 messages.ERROR,
                                 "Submitted form is not valid! Try again.")
            return render(request, 'dashboard/edit_product.html')
    else:
        form = ProductForm(instance=product, initial={
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_image': product.product_image,
            'quantity': product.quantity,
            'product_available': product.product_available,
            'product_description': product.product_description
        })
        return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})


@group_required('officer_group')
def logout_view(request):
    logout(request)
    return render(request, 'core/login.html')
