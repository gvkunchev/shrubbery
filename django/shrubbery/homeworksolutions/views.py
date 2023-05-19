from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from homeworks.models import Homework
from .models import HomeworkSolution
from .forms import HomeworkSolutionForm


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


def add_homework_solution(request, homework):
    """Add homework solution page."""
    try:
        homework = Homework.objects.get(pk=homework)
        if not homework.can_upload:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework
    }
    if request.method == 'POST':
        data = {
            'author': request.user,
            'homework': homework,
        }
        try:
            # If there is already an uploaded solution,
            # move it to history and replace with the new one
            existing_solution = HomeworkSolution.objects.get(author=request.user, homework=homework)
            existing_solution.send_to_history()
            form = HomeworkSolutionForm(data, request.FILES, instance=existing_solution)
        except ObjectDoesNotExist:
            form = HomeworkSolutionForm(data, request.FILES)
        if form.is_valid():
            solution = form.save()
            return redirect(f'/homework/{homework.pk}/solution/{solution.pk}')
        else:
            context['errors'] = form.errors
    return render(request, "homework_solutions/add_solution.html", context)
