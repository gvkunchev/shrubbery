from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


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

def settings(request):
    '''Profile settings.'''
    return render(request, "auth/settings.html")
