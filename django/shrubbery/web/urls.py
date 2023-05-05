from django.urls import re_path
from . import views

app_name = 'web'
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^news$', views.news, name='news'),
    re_path(r'^materials$', views.materials, name='materials'),
    re_path(r'^users$', views.users, name='users'),
]
