from django.urls import re_path

from . import views


app_name = 'activity'


urlpatterns = [
    re_path(r'^activity$', views.activity, name='activity'),
    re_path(r'^activity/(?P<activity>\d+)/force_seen$', views.force_seen, name='force_seen'),
]
