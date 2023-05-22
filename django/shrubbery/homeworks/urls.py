from django.urls import re_path

from . import views


app_name = 'homeworks'


urlpatterns = [
    re_path(r'^homeworks$', views.homeworks, name='homeworks'),
    re_path(r'^homework/(?P<homework>\d+)$', views.homework, name='homework'),
    re_path(r'^homework/add$', views.add_homework, name='add_homework'),
    re_path(r'^homework/edit/(?P<homework>\d+)$', views.edit_homework, name='edit_homework'),
    re_path(r'^homework/delete/(?P<homework>\d+)$', views.delete_homework, name='delete_homework'),
    re_path(r'^homework_comment/edit/(?P<comment>\d+)$', views.EditHomeworkComment.as_view(), name='edit_homework_comment'),
    re_path(r'^homework_comment/delete/(?P<comment>\d+)$', views.DeleteHomeworkComment.as_view(), name='delete_homework_comment'),
    re_path(r'^homework_comment/add$', views.AddHomeworkComment.as_view(), name='add_homework_comment'),
    re_path(r'^homework_comment/(?P<comment>\d+)/star/add$', views.AddHomeworkCommentStar.as_view(), name='add_homework_comment_star'),
    re_path(r'^homework_comment/(?P<comment>\d+)/star/remove$', views.RemoveHomeworkCommentStar.as_view(), name='remove_homework_comment_star'),
]
