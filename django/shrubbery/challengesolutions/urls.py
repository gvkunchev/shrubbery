from django.urls import re_path

from . import views


app_name = 'challengesolutions'


urlpatterns = [
    re_path(r'^challenge/(?P<challenge>\d+)/solutions$', views.challenge_solutions, name='challenge_solutions'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)$', views.challenge_solution, name='challenge_solution'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/add$', views.add_challenge_solution, name='add_challenge_solution'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/edit$', views.EditChallengeSolutionComment.as_view(), name='edit_challenge_solution_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/delete$', views.DeleteChallengeSolutionComment.as_view(), name='delete_challenge_solution_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/comment/add$', views.AddChallengeSolutionComment.as_view(), name='add_challenge_solution_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/star/add$', views.AddChallengeSolutionCommentStar.as_view(), name='add_challenge_solution_comment_star'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/star/remove$', views.RemoveChallengeSolutionCommentStar.as_view(), name='remove_challenge_solution_comment_star'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/inlinecomment/(?P<comment>\d+)/edit$', views.EditChallengeSolutionInlineComment.as_view(), name='edit_challenge_solution_inline_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/inlinecomment/(?P<comment>\d+)/delete$', views.DeleteChallengeSolutionInlineComment.as_view(), name='delete_challenge_solution_inline_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/inlinecomment/add$', views.AddChallengeSolutionInlineComment.as_view(), name='add_challenge_solution_inline_comment'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/set_teacher_points$', views.set_teacher_points, name='set_teacher_points'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/subscribe$', views.subscribe, name='subscribe'),
    re_path(r'^challenge/(?P<challenge>\d+)/solution/(?P<solution>\d+)/unsubscribe$', views.unsubscribe, name='unsubscribe'),
]
