from django.urls import re_path

from . import views


app_name = 'forum'


urlpatterns = [
    re_path(r'^forums$', views.forums, name='forums'),
    re_path(r'^forum/(?P<forum>\d+)$', views.forum, name='forum'),
    re_path(r'^forum/(?P<forum>\d+)/delete$', views.delete_forum, name='delete_forum'),
    re_path(r'^forum/(?P<forum>\d+)/edit$', views.edit_forum, name='edit_forum'),
    re_path(r'^forum/add$', views.add_forum, name='add_forum'),
    re_path(r'^forum/(?P<forum>\d+)/comment/(?P<comment>\d+)/edit$', views.EditForumComment.as_view(), name='edit_forum_comment'),
    re_path(r'^forum/(?P<forum>\d+)/comment/(?P<comment>\d+)/delete$', views.DeleteForumComment.as_view(), name='delete_forum_comment'),
    re_path(r'^forum/(?P<forum>\d+)/comment/(?P<parent>\d+)/answer$', views.answer_forum_comment, name='answer_forum_comment'),
    re_path(r'^forum/(?P<forum>\d+)/comment/add$', views.AddForumComment.as_view(), name='add_forum_comment'),
    re_path(r'^forum/(?P<forum>\d+)/comment/(?P<comment>\d+)/star/add$', views.AddForumCommentStar.as_view(), name='add_forum_comment_star'),
    re_path(r'^forum/(?P<forum>\d+)/comment/(?P<comment>\d+)/star/remove$', views.RemoveForumCommentStar.as_view(), name='remove_forum_comment_star'),
]
