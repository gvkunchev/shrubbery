from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from news.models import NewsArticle


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "missing.html")


def home(request):
    '''Home page.'''
    return render(request, "home.html", {'news': NewsArticle.objects.all()})


def materials(request):
    '''Materials page.'''
    return render(request, "materials.html")


def users(request):
    '''Users page.'''
    return render(request, "users.html")


def news(request):
    '''News page.'''
    return render(request, "news/news.html", {'news': NewsArticle.objects.all()})


def news_article(request, article):
    '''News article page.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "news/news_article.html", {'article': article})
