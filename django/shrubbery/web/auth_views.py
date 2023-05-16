from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import PasswordChangeForm

from users.forms import EditUserForm, PasswordSetForm, RegisterStudent
from users.emails import send_activation_email
from users.models import User, Student
from users.tokens import account_activation_token


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


def activate(request):
    """Activate an account."""
    if request.method == 'GET':
        try:
            uidb64 = request.GET['uidb64']
            token = request.GET['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'auth/activated.html', {'correct': True})
        else:
            return render(request, 'auth/activated.html', {'correct': False})
    else:
        try:
            uidb64 = request.POST['uidb64']
            token = request.POST['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(request.POST['uidb64'])
            print(request.POST['token'])
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = PasswordSetForm(user, request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                login(request, user)
                update_session_auth_hash(request, user)
                return render(request, "home.html", {'welcome': True})
            else:
                context = {
                    'correct': True,
                    'errors': form.errors
                }
                return render(request, 'auth/activated.html', context)
        else:
            return render(request, 'auth/activated.html', {'correct': False})


@login_required
def settings(request):
    '''Profile settings.'''
    if request.method == 'POST':
        if 'personal_info' in request.POST:
            # If these checks are missing, users can upload new images, but the
            # image is not processed. Image uploda happens before validation so
            # they can upload files without any validation being done.
            # There is already front-end validation that requires inputing these fields.
            # This is just in case.
            if 'first_name' not in request.POST or request.POST['first_name'] == '':
                return redirect('web:missing')
            if 'last_name' not in request.POST or request.POST['last_name'] == '':
                return redirect('web:missing')
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


def register(request):
    """Student form for registering their email."""
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            fn = request.POST['fn'].strip()
            user = Student.objects.get(first_name=first_name, last_name=last_name, fn=fn)
        except Exception as e:
            context = {
                'error': 'Липсваш от списъка.'
            }
            return render(request, "auth/register.html", context)
        if user.is_active:
            context = {
                'error': 'Вече си регистриран.'
            }
            return render(request, "auth/register.html", context)
        form = RegisterStudent(request.POST, instance=user)
        if form.is_valid():
            form.save()
            send_activation_email(request, user)
            context = {
                'info': 'Изпратен е имейл за активация.'
            }
        else:
            context = {
                'errors': form.errors
            }
        return render(request, "auth/register.html", context)
    else:
        return render(request, "auth/register.html")