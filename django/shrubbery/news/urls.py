from django.urls import re_path
from . import views


app_name = 'news'


urlpatterns = [
    re_path(r'^news$', views.news, name='news'),
    re_path(r'^news/add$', views.add_news_article, name='add_news_article'),
    re_path(r'^news/(?P<article>\d+)/delete$', views.delete_news_article, name='delete_news_article'),
    re_path(r'^news/(?P<article>\d+)/edit$', views.edit_news_article, name='edit_news_article'),
    re_path(r'^news/(?P<article>\d+)$', views.news_article, name='news_article'),
]
