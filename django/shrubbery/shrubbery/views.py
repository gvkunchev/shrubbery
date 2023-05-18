from django.shortcuts import render

from points.getters import get_rank_and_points
from news.models import NewsArticle


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "backbone/missing.html")


def home(request):
    '''Home page.'''
    MAX_NEWS = 5
    context = {
        'news': NewsArticle.objects.all()[:MAX_NEWS]
    }
    if request.user.is_authenticated and request.user.is_student:
        context.update({
            'ranking': get_rank_and_points(request.user)
        })
    return render(request, "home.html", context)
