from django.urls import re_path

from . import views


app_name = 'activity'


urlpatterns = [
    re_path(r'^activity$', views.activity, name='activity')
]
