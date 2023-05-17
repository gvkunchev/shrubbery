from django.urls import re_path
from . import views


app_name = 'vouchers'


urlpatterns = [
    re_path(r'^vouchers$', views.vouchers, name='vouchers'),
    re_path(r'^vouchers/add$', views.add_vouchers, name='add_vouchers'),
    re_path(r'^vouchers/remove$', views.remove_vouchers, name='remove_vouchers'),
    re_path(r'^redeemed$', views.redeemed, name='redeemed'),
    re_path(r'^redeem$', views.redeem, name='redeem'),
]
