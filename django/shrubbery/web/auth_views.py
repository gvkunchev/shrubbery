from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from users.forms import EditUserForm


def login_(request):
    '''Login page.'''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            return render(request, "auth/login.html",
                          {'errors': 'unauthorized'})
        else:
            login(request, user)
            try:
                return redirect(request.GET['next'])
            except KeyError:
                return redirect('/')
    else:
        return render(request, "auth/login.html")


def logout_(request):
    '''Logut.'''
    logout(request)
    return redirect('/')


@login_required
def settings(request):
    '''Profile settings.'''
    if request.method == 'POST':
        if 'personal_info' in request.POST:
            form = EditUserForm(request.POST, request.FILES, instance=request.user)
            context = {}
            if form.is_valid():
                form.save()
                context = {
                    'settings_info': 'Настройките са запазени'
                }
            else:
                context = {
                    'errors': form.errors
                }
            return render(request, "auth/settings.html", context)
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                context = {
                    'password_info': 'Паролата е сменена'
                }
            else:
                context = {
                    'errors': form.errors
                }
            return render(request, "auth/settings.html", context)
        else:
            return redirect('web:missing')
    else:
        return render(request, "auth/settings.html")
