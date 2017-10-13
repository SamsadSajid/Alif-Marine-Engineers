# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .form import SignUpForm
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html',
                          {'form': form})

        else:
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            # User.objects.create_user(username=username, password=password,
            #                          email=email)
            # user = authenticate(username=username, password=password)
            # login(request, user)
            user.is_active = False
            user.save()
            # login(request, user)

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'noreply@Alif-Marine-Engineers.co', [email])

            return redirect('account_activation_sent')
            # return redirect('/')

    else:
        return render(request, 'signup.html',
                      {'form': SignUpForm()})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        # welcome_post = '{0} has joined the network.'.format(user.username,
        #                                                     user.username)
        # feed = Feed(user=user, post=welcome_post)
        # feed.save()
        # return render(request, 'redirect-login.html')
        return redirect('/pass?=success/')
    else:
        return render(request, 'account_activation_invalid.html')


def regSuccess(request):
    return render(request, 'redirect-login.html')




