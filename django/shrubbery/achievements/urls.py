from django.urls import re_path

from . import views


app_name = 'achievements'


urlpatterns = [
    re_path(r'^achievements$', views.achievements, name='achievements')
]
