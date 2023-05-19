from django.urls import re_path

from . import views


app_name = 'homeworksolutions'


urlpatterns = [
    re_path(r'^homework/(?P<homework>\d+)/solutions$', views.homework_solutions, name='homework_solutions'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)$', views.homework_solution, name='homework_solution'),
    re_path(r'^homework/(?P<homework>\d+)/solution/add$', views.add_homework_solution, name='add_homework_solution'),
]
