from django.urls import re_path

from . import views


app_name = 'resources'


urlpatterns = [
    re_path(r'^resources$', views.resources, name='resources'),
    re_path(r'^resource/add$', views.add_resource, name='add_resource'),
    re_path(r'^resource/remove$', views.remove_resources, name='remove_resources'),
]
