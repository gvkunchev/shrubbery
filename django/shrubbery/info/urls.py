from django.urls import re_path

from . import views


app_name = 'info'


urlpatterns = [
    re_path(r'^info$', views.info, name='info'),
    re_path(r'^info/showdown$', views.info_showdown, name='info_showdown'),
    re_path(r'^info/code$', views.info_code, name='info_code'),
]
