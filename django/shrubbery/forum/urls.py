from django.urls import re_path

from . import views


app_name = 'forum'


urlpatterns = [
    re_path(r'^forums$', views.forums, name='forums'),
    re_path(r'^forum/(?P<forum>\d+)$', views.forum, name='forum'),
    re_path(r'^forum/delete/(?P<forum>\d+)$', views.delete_forum, name='delete_forum'),
    re_path(r'^forum/edit/(?P<forum>\d+)$', views.edit_forum, name='edit_forum'),
    re_path(r'^forum_comment/(?P<comment>\d+)/star/add$', views.add_forum_comment_star, name='add_forum_comment_star'),
    re_path(r'^forum_comment/(?P<comment>\d+)/star/remove$', views.remove_forum_comment_star, name='remove_forum_comment_star'),
    re_path(r'^forum/add$', views.add_forum, name='add_forum'),
    re_path(r'^forum_comment/edit/(?P<comment>\d+)$', views.edit_forum_comment, name='edit_forum_comment'),
    re_path(r'^forum_comment/delete/(?P<comment>\d+)$', views.delete_forum_comment, name='delete_forum_comment'),
    re_path(r'^forum_comment/add$', views.add_forum_comment, name='add_forum_comment'),
]
