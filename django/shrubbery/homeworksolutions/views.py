from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from homeworks.models import Homework
from .models import HomeworkSolution


def homework_solutions(request, homework):
    """Homework solutions page."""
    try:
        homework = Homework.objects.get(pk=homework)
        if homework.hidden or not homework.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.user.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework,
        'solutions': HomeworkSolution.objects.filter(homework=homework)
    }
    return render(request, "homework_solutions/solutions.html", context)


def homework_solution(request, homework, solution):
    """Homework solution page."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
        if homework.hidden or not homework.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if request.user.is_student and request.user.pk != solution.author.pk:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework,
        'solution': solution
    }
    return render(request, "homework_solutions/solution.html", context)
