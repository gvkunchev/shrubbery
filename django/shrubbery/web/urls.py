from django.urls import re_path
from . import views
from . import auth_views
from . import teacher_views


app_name = 'web'


urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^missing$', views.missing, name='missing'),
    re_path(r'^news$', views.news, name='news'),
    re_path(r'^news/add$', teacher_views.add_news_article, name='add_news_article'),
    re_path(r'^news/delete/(?P<article>\d+)$', teacher_views.delete_news_article, name='delete_news_article'),
    re_path(r'^news/edit/(?P<article>\d+)$', teacher_views.edit_news_article, name='edit_news_article'),
    re_path(r'^news/(?P<article>\d+)$', views.news_article, name='news_article'),
    re_path(r'^materials$', views.materials, name='materials'),
    re_path(r'^students$', views.students, name='students'),
    re_path(r'^student/(?P<student>\d+)$', views.student, name='student'),
    re_path(r'^teachers$', views.teachers, name='teachers'),
    re_path(r'^teacher/(?P<teacher>\d+)$', views.teacher, name='teacher'),
    re_path(r'^participants$', teacher_views.participants, name='participants'),
    re_path(r'^add_participant$', teacher_views.add_participant, name='add_participant'),
    re_path(r'^add_participants$', teacher_views.add_participants, name='add_participants'),
    re_path(r'^participant/(?P<participant>\d+)$', teacher_views.participant, name='participant'),
    re_path(r'^team$', teacher_views.team, name='team'),
    re_path(r'^team_member/(?P<teacher>\d+)$', teacher_views.team_member, name='team_memeber'),
    re_path(r'^login$', auth_views.login_, name='login'),
    re_path(r'^logout$', auth_views.logout_, name='logout'),
    re_path(r'^settings$', auth_views.settings, name='settings'),
]
