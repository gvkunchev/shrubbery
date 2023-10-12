from django.urls import re_path

from . import views


app_name = 'points'


urlpatterns = [
    re_path(r'^points$', views.points, name='points'),
    re_path(r'^my_points$', views.my_points, name='my_points'),
    re_path(r'^scoreboard$', views.scoreboard, name='scoreboard'),
]
