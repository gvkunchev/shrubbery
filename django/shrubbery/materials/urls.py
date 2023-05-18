from django.urls import re_path
from . import views


app_name = 'materials'


urlpatterns = [
    re_path(r'^materials$', views.materials, name='materials'),
    re_path(r'^lectures$', views.lectures, name='lectures'),
    re_path(r'^lecture/(?P<lecture>\d+)$', views.lecture, name='lecture'),
    re_path(r'^lecture/add$', views.add_lecture, name='add_lecture'),
]
