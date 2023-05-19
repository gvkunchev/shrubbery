"""
URL configuration for shrubbery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views


handler404 = 'shrubbery.views.missing'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('', include('forum.urls')),
    path('', include('users.urls')),
    path('', include('materials.urls')),
    path('', include('vouchers.urls')),
    path('', include('points.urls')),
    path('', include('resources.urls')),
    path('', include('exams.urls')),
    path('', include('homeworks.urls')),
    path('', include('homeworksolutions.urls')),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^missing$', views.missing, name='missing')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
