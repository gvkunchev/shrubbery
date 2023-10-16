from django.urls import re_path

from . import views


app_name = 'homeworks'


urlpatterns = [
    re_path(r'^homeworks$', views.homeworks, name='homeworks'),
    re_path(r'^homework/(?P<homework>\d+)$', views.homework, name='homework'),
    re_path(r'^homework/(?P<homework>\d+)/run_tests$', views.run_tests, name='run_tests'),
    re_path(r'^homework/(?P<homework>\d+)/get_slackers$', views.get_slackers, name='get_slackers'),
    re_path(r'^homework/add$', views.add_homework, name='add_homework'),
    re_path(r'^homework/(?P<homework>\d+)/edit$', views.edit_homework, name='edit_homework'),
    re_path(r'^homework/(?P<homework>\d+)/delete$', views.delete_homework, name='delete_homework'),
    re_path(r'^homework/(?P<homework>\d+)/comment/(?P<comment>\d+)/edit$', views.EditHomeworkComment.as_view(), name='edit_homework_comment'),
    re_path(r'^homework/(?P<homework>\d+)/comment/(?P<comment>\d+)/delete$', views.DeleteHomeworkComment.as_view(), name='delete_homework_comment'),
    re_path(r'^homework/(?P<homework>\d+)/comment/add$', views.AddHomeworkComment.as_view(), name='add_homework_comment'),
    re_path(r'^homework/(?P<homework>\d+)/comment/(?P<comment>\d+)/star/add$', views.AddHomeworkCommentStar.as_view(), name='add_homework_comment_star'),
    re_path(r'^homework/(?P<homework>\d+)/comment/(?P<comment>\d+)/star/remove$', views.RemoveHomeworkCommentStar.as_view(), name='remove_homework_comment_star'),
    
]
