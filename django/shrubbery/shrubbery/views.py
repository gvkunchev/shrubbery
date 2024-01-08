from django.shortcuts import render
from django.conf import settings

from points.getters import get_rank_and_points
from homeworks.getters import get_active_homeworks
from challenges.getters import get_active_challenges
from news.models import NewsArticle
from users.models import Student


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "backbone/missing.html")


def home(request):
    '''Home page.'''
    MAX_NEWS = 5
    context = {
        'news': NewsArticle.objects.all()[:MAX_NEWS]
    }
    if request.user.is_authenticated and request.user.is_student:
        context.update({
            'ranking': get_rank_and_points(request.user)
        })
    if request.user.is_authenticated:
        context.update({
            'active_homeworks': get_active_homeworks()
        })
        context.update({
            'active_challenges': get_active_challenges()
        })
    if request.user.is_authenticated and request.user.is_student and settings.SHOW_FINAL_SCHEDULE:
        student = Student.objects.get(pk=request.user.pk)
        try:
            slot = student.finalscheduleslot_set.get()
            context.update({
                'final_countdown': slot.start
            })
        except:
            pass # Not in the schedule
    return render(request, "home.html", context)
