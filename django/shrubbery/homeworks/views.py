import os
import subprocess
import sys


from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse


from shrubbery.view_decorators import is_teacher

from .models import Homework, HomeworkComment
from .forms import HomeworkForm, HomeworkCommentForm

from comments.views import AddComment, EditComment, DeleteComment, SetCommentStar

from .tasks import run_homework_tests


def homeworks(request):
    '''Homeworks page.'''
    return render(request, "homeworks/homeworks.html", {'homeworks': Homework.objects.all()})


@is_teacher
def add_homework(request):
    '''Add new homework.'''
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'author': request.user})
        form = HomeworkForm(data)
        if form.is_valid():
            form.save()
            context = {
                'homeworks': Homework.objects.all(),
                'info': 'Успешно добави домашно'
            }
            return render(request, "homeworks/homeworks.html", context)
        else:
            return render(request, "homeworks/add_homework.html", {'errors': form.errors})
    else:
        return render(request, "homeworks/add_homework.html")


def homework(request, homework):
    '''Homework page.'''
    try:
        homework = Homework.objects.get(pk=homework)
        if homework.hidden and not (request.user.is_authenticated and request.user.is_teacher):
            raise ObjectDoesNotExist()
        paginator = Paginator(homework.comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "homeworks/homework.html", {'homework': homework, 'comments': page_obj})


@is_teacher
def delete_homework(request, homework):
    '''Delete homework.'''
    try:
        homework = Homework.objects.get(pk=homework)
    except ObjectDoesNotExist:
        return redirect('missing')
    if len(homework.homeworksolution_set.values()):
        context = {
            'homeworks': Homework.objects.all(),
            'error': 'Не можеш да изтриеш домашано с вече предадени решения. Използвай конзолата.'
        }
    else:
        homework.delete()
        context = {
            'homeworks': Homework.objects.all(),
            'info': 'Успешно изтри домашно'
        }
    return render(request, "homeworks/homeworks.html", context)


@is_teacher
def edit_homework(request, homework):
    '''Edit homework.'''
    try:
        homework = Homework.objects.get(pk=homework)
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework
    }
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'author': request.user})
        form = HomeworkForm(data, instance=homework)
        if form.is_valid():
            form.save()
            context['info'] = 'Успешно редактира домашно'
        else:
            context['errors'] = form.errors
    return render(request, "homeworks/edit_homework.html", context)


class AddHomeworkComment(AddComment):
    HOST = Homework
    FORM = HomeworkCommentForm
    HOST_KEY = 'homework'


class EditHomeworkComment(EditComment):
    HOST = Homework
    FORM = HomeworkCommentForm
    HOST_KEY = 'homework'
    COMMENT_MODEL = HomeworkComment
    TEMPLATE = 'homeworks/edit_homework_comment.html'


class DeleteHomeworkComment(DeleteComment):
    HOST_KEY = 'homework'
    COMMENT_MODEL = HomeworkComment


class AddHomeworkCommentStar(SetCommentStar):
    HOST_KEY = 'homework'
    COMMENT_MODEL = HomeworkComment
    STATUS = True


class RemoveHomeworkCommentStar(SetCommentStar):
    HOST_KEY = 'homework'
    COMMENT_MODEL = HomeworkComment
    STATUS = False


@is_teacher
def run_tests(request, homework):
    '''Run homework tests.'''
    try:
        homework = Homework.objects.get(pk=homework)
        if homework.executing_tests:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        return redirect('missing')
    homework.executing_tests = True
    homework.save()
    if os.environ.get('SHRUBBERY_ENV') == 'prd':
        run_homework_tests.delay(homework.pk)
    else:
        run_homework_tests(homework.pk)
    return redirect(request.GET.get('goto', f'/homework/{homework.pk}'))


@is_teacher
def get_slackers(request, homework):
    '''Compare solutions and get slackers report..'''
    try:
        homework = Homework.objects.get(pk=homework)
    except ObjectDoesNotExist:
        return redirect('missing')
    path = os.path.join(settings.MEDIA_ROOT, 'homeworksolutions', str(homework.pk))
    slackers_run = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'slackers.py'), path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = slackers_run.communicate()
    return HttpResponse(stdout)