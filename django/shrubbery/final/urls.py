from django.urls import re_path

from . import views


app_name = 'final'


urlpatterns = [
    re_path(r'^final/schedule_editor$', views.schedule_editor, name='schedule_editor'),
    re_path(r'^final/schedule$', views.schedule, name='schedule'),
    re_path(r'^final/slot/add$', views.add_slot, name='add_slot'),
    re_path(r'^final/slots/add$', views.add_slots, name='add_slots'),
    re_path(r'^final/slot/remove/(?P<slot>\d+)$', views.remove_slot, name='remove_slot'),
    re_path(r'^final/slot/edit/(?P<slot>\d+)$', views.edit_slot, name='edit_slot'),
    re_path(r'^final/slot/edit/(?P<slot>\d+)/remove/(?P<student>\d+)$', views.remove_student, name='remove_student'),
    re_path(r'^final/slot/edit/(?P<slot>\d+)/add$', views.add_student, name='add_student'),
    re_path(r'^final/exchange/request/(?P<student>\d+)$', views.request_exchange, name='request_exchange'),
    re_path(r'^final/exchange/cancel/(?P<student>\d+)$', views.cancel_exchange, name='cancel_exchange'),
    re_path(r'^final/exchange/confirm/(?P<student>\d+)$', views.confirm_exchange, name='confirm_exchange'),
]
