from django.urls import re_path

from . import views


app_name = 'challenges'


urlpatterns = [
    re_path(r'^challenges$', views.challenges, name='challenges'),
    re_path(r'^challenge/(?P<challenge>\d+)$', views.challenge, name='challenge'),
    re_path(r'^challenge/(?P<challenge>\d+)/run_tests$', views.run_tests, name='run_tests'),
    re_path(r'^challenge/(?P<challenge>\d+)/get_slackers$', views.get_slackers, name='get_slackers'),
    re_path(r'^challenge/add$', views.add_challenge, name='add_challenge'),
    re_path(r'^challenge/(?P<challenge>\d+)/edit$', views.edit_challenge, name='edit_challenge'),
    re_path(r'^challenge/(?P<challenge>\d+)/delete$', views.delete_challenge, name='delete_challenge'),
    re_path(r'^challenge/(?P<challenge>\d+)/comment/(?P<comment>\d+)/edit$', views.EditChallengeComment.as_view(), name='edit_challenge_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/comment/(?P<comment>\d+)/delete$', views.DeleteChallengeComment.as_view(), name='delete_challenge_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/comment/add$', views.AddChallengeComment.as_view(), name='add_challenge_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/comment/(?P<comment>\d+)/star/add$', views.AddChallengeCommentStar.as_view(), name='add_challenge_comment_star'),
    re_path(r'^challenge/(?P<challenge>\d+)/comment/(?P<comment>\d+)/star/remove$', views.RemoveChallengeCommentStar.as_view(), name='remove_challenge_comment_star'),
    
]
