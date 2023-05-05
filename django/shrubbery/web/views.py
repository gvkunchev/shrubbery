from django.shortcuts import render


def home(request):
    '''Home page.'''
    return render(request, "home.html")


def materials(request):
    '''Materials page.'''
    return render(request, "materials.html")


def users(request):
    '''Users page.'''
    return render(request, "users.html")


def news(request):
    '''News page.'''
    return render(request, "news.html")
