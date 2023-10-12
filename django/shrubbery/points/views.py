from django.shortcuts import render

from shrubbery.view_decorators import is_teacher, is_student

from exams.models import Exam
from homeworks.models import Homework
from challenges.models import Challenge

from .getters import get_scoreboard_summary


@is_teacher
def points(request):
    '''Points page.'''
    context = {
        'data': get_scoreboard_summary(),
        'exams': Exam.objects.all(),
        'homeworks': Homework.objects.filter(verified=True).reverse(),
        'challenges': Challenge.objects.filter(verified=True).reverse()
    }
    return render(request, "points/points.html", context)


@is_student
def my_points(request):
    '''Student's points page.'''
    for student_data in get_scoreboard_summary():
        if student_data['student'].pk == request.user.pk:
            data = student_data
            break
    else:
        data = None
    context = {
        'data': data,
        'exams': Exam.objects.all(),
        'homeworks': Homework.objects.filter(verified=True).reverse(),
        'challenges': Challenge.objects.filter(verified=True).reverse()
    }
    return render(request, "points/my_points.html", context)


def scoreboard(request):
    '''Points page.'''
    return render(request, "scoreboard.html", {'data': get_scoreboard_summary()})
