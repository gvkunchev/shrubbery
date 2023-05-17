from django.shortcuts import render

from news.models import NewsArticle


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "backbone/missing.html")


def home(request):
    '''Home page.'''
    MAX_NEWS = 5
    return render(request, "home.html", {'news': NewsArticle.objects.all()[:MAX_NEWS]})
