from django.urls import re_path
from . import views


app_name = 'news'


urlpatterns = [
    re_path(r'^news$', views.news, name='news'),
    re_path(r'^news/add$', views.add_news_article, name='add_news_article'),
    re_path(r'^news/delete/(?P<article>\d+)$', views.delete_news_article, name='delete_news_article'),
    re_path(r'^news/edit/(?P<article>\d+)$', views.edit_news_article, name='edit_news_article'),
    re_path(r'^news/(?P<article>\d+)$', views.news_article, name='news_article'),
]
