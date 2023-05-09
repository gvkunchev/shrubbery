from django.urls import re_path
from . import views

app_name = 'web'

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^missing$', views.missing, name='missing'),
    re_path(r'^news$', views.news, name='news'),
    re_path(r'^news/(?P<article>\d+)$', views.news_article, name='news_article'),
    re_path(r'^materials$', views.materials, name='materials'),
    re_path(r'^students$', views.students, name='students'),
    re_path(r'^student/(?P<student>\d+)$', views.student, name='student'),
    re_path(r'^teachers$', views.teachers, name='teachers'),
    re_path(r'^teacher/(?P<teacher>\d+)$', views.teacher, name='teacher'),
]
