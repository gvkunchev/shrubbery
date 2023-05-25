from django.shortcuts import render

from shrubbery.view_decorators import is_teacher

from exams.models import Exam
from homeworks.models import Homework

from .getters import get_scoreboard_summary


@is_teacher
def points(request):
    '''Points page.'''
    context = {
        'data': get_scoreboard_summary(),
        'exams': Exam.objects.all(),
        'homeworks': Homework.objects.filter(verified=True).reverse()
    }
    return render(request, "points/points.html", context)


def scoreboard(request):
    '''Points page.'''
    return render(request, "scoreboard.html", {'data': get_scoreboard_summary()})
