from django.urls import re_path

from . import views


app_name = 'exams'


urlpatterns = [
    re_path(r'^exams$', views.exams, name='exams'),
    re_path(r'^exam/(?P<exam>\d+)$', views.exam, name='exam'),
    re_path(r'^exam/add$', views.add_exam, name='add_exam'),
    re_path(r'^exam/(?P<exam>\d+)/edit$', views.edit_exam, name='edit_exam'),
    re_path(r'^exam/(?P<exam>\d+)/delete$', views.delete_exam, name='delete_exam'),
    re_path(r'^exam/results/delete$', views.delete_exam_results, name='delete_exam_results'),
    re_path(r'^exam/result/add$', views.add_exam_result, name='add_exam_result'),
    re_path(r'^exam/results/add$', views.add_exam_results, name='add_exam_results'),
]
