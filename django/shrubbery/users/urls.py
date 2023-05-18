from django.urls import re_path

from . import views


app_name = 'users'


urlpatterns = [
    re_path(r'^login$', views.login_, name='login'),
    re_path(r'^logout$', views.logout_, name='logout'),
    re_path(r'^activate$', views.activate, name='activate'),
    re_path(r'^register$', views.register, name='register'),
    re_path(r'^settings$', views.settings, name='settings'),
    re_path(r'^students$', views.students, name='students'),
    re_path(r'^student/(?P<student>\d+)$', views.student, name='student'),
    re_path(r'^teachers$', views.teachers, name='teachers'),
    re_path(r'^teacher/(?P<teacher>\d+)$', views.teacher, name='teacher'),
    re_path(r'^participants$', views.participants, name='participants'),
    re_path(r'^participant/(?P<participant>\d+)$', views.participant, name='participant'),
    re_path(r'^participant/add$', views.add_participant, name='add_participant'),
    re_path(r'^participants/add$', views.add_participants, name='add_participants'),
    re_path(r'^team$', views.team, name='team'),
    re_path(r'^team/member/(?P<teacher>\d+)$', views.team_member, name='team_memeber'),
    re_path(r'^team/member/add$', views.add_team_member, name='add_team_member'),
]
