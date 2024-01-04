from django.urls import re_path

from . import views


app_name = 'homeworksolutions'


urlpatterns = [
    re_path(r'^homework/(?P<homework>\d+)/solutions$', views.homework_solutions, name='homework_solutions'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)$', views.homework_solution, name='homework_solution'),
    re_path(r'^homework/(?P<homework>\d+)/solution/add$', views.add_homework_solution, name='add_homework_solution'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/edit$', views.EditHomeworkSolutionComment.as_view(), name='edit_homework_solution_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/delete$', views.DeleteHomeworkSolutionComment.as_view(), name='delete_homework_solution_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/comment/add$', views.AddHomeworkSolutionComment.as_view(), name='add_homework_solution_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/star/add$', views.AddHomeworkSolutionCommentStar.as_view(), name='add_homework_solution_comment_star'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/comment/(?P<comment>\d+)/star/remove$', views.RemoveHomeworkSolutionCommentStar.as_view(), name='remove_homework_solution_comment_star'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/inlinecomment/(?P<comment>\d+)/edit$', views.EditHomeworkSolutionInlineComment.as_view(), name='edit_homework_solution_inline_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/inlinecomment/(?P<comment>\d+)/delete$', views.DeleteHomeworkSolutionInlineComment.as_view(), name='delete_homework_solution_inline_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/inlinecomment/add$', views.AddHomeworkSolutionInlineComment.as_view(), name='add_homework_solution_inline_comment'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/set_teacher_points$', views.set_teacher_points, name='set_teacher_points'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/edit_internal_notes$', views.edit_internal_notes, name='edit_internal_notes'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/subscribe$', views.subscribe, name='subscribe'),
    re_path(r'^homework/(?P<homework>\d+)/solution/(?P<solution>\d+)/unsubscribe$', views.unsubscribe, name='unsubscribe'),
]
