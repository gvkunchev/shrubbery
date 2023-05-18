from django.shortcuts import render

from shrubbery.view_decorators import is_teacher

from .getters import get_scoreboard_summary


@is_teacher
def points(request):
    '''Points page.'''
    return render(request, "points/points.html", {'data': get_scoreboard_summary()})


def scoreboard(request):
    '''Points page.'''
    return render(request, "scoreboard.html", {'data': get_scoreboard_summary()})
