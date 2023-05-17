from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from shrubbery.view_decorators import is_teacher

from .models import NewsArticle
from .forms import NewsArticleForm


def news(request):
    '''News page.'''
    all_news = NewsArticle.objects.all()
    paginator = Paginator(all_news, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "news/news.html", {'news': page_obj})


def news_article(request, article):
    '''News article page.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "news/news_article.html", {'article': article})


@is_teacher
def add_news_article(request):
    '''Add news article.'''
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = NewsArticleForm(data)
        if form.is_valid():
            form.save()
            return redirect('news:news')
        else:
            return render(request, "news/add_news_article.html", {'errors': form.errors})
    else:
        return render(request, "news/add_news_article.html")


@is_teacher
def delete_news_article(request, article):
    '''Delete news article.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('missing')
    article.delete()
    return redirect('news:news')


@is_teacher
def edit_news_article(request, article):
    '''Edit news article.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = NewsArticleForm(data, instance=article)
        if form.is_valid():
            form.save()
            return redirect(f'/news/{article.pk}')
        else:
            context = {
                'article': article,
                'errors': form.errors
            }
            return render(request, "news/edit_news_article.html", context)
    else:
        return render(request, "news/edit_news_article.html", {'article': article})
