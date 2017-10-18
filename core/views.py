import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from PIL import Image
from django.contrib.auth import authenticate, login

from .form import LogInForm


def home(request):
    if request.user.is_authenticated():
        return render(request, 'redirect-login.html')
    else:
        return render(request, 'base.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.profile.account_type == 0:
                    login(request, user)
                    print("yoo")
            # return render(request, 'dashboard/profile.html')
                    return redirect('/client/profile/')
                elif user.profile.account_type == 1:
                    login(request, user)
                    print("yoo")
                    # return render(request, 'dashboard/profile.html')
                    return redirect('/officer/profile/')
                elif user.profile.account_type == 2:
                    login(request, user)
                    print("yoo")
                    # return render(request, 'dashboard/profile.html')
                    return redirect('/service/profile/')
                elif user.profile.account_type == 3:
                    login(request, user)
                    print("yoo")
                    # return render(request, 'dashboard/profile.html')
                    return redirect('/production/profile/')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     "Your account is not active. Please contact immediately"
                                     "to the help centre!")
                return render(request, 'core/login.html')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 "Username or Password doesn't match")
            return render(request, 'core/login.html')
    else:
        return render(request, 'core/login.html')


@login_required(login_url='/login/')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'client/client_profile.html', {
        'user': user,
    })

