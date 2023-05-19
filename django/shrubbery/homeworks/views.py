from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from .models import Homework, HomeworkComment
from .forms import HomeworkForm, HomeworkCommentForm


def homeworks(request):
    '''Homeworks page.'''
    return render(request, "homeworks/homeworks.html", {'homeworks': Homework.objects.all()})


@is_teacher
def add_homework(request):
    '''Add new homework.'''
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
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
        form = HomeworkForm(request.POST, instance=homework)
        if form.is_valid():
            form.save()
            context['info'] = 'Успешно редактира домашно'
        else:
            context['errors'] = form.errors
    return render(request, "homeworks/edit_homework.html", context)

@login_required
def add_homework_comment(request):
    '''Add homework comment.'''
    if request.method != 'POST':
        return redirect('missing')
    try:
        homework = Homework.objects.get(pk=request.POST.get('homework'))
    except ObjectDoesNotExist:
            return redirect('missing')
    data = {
        'content': request.POST.get('content'),
        'homework': request.POST.get('homework'),
        'author': request.user
    }
    form = HomeworkCommentForm(data)
    if form.is_valid():
        comment = form.save()
    return redirect(f'/homework/{homework.pk}#comment{comment.pk}')


@login_required
def edit_homework_comment(request, comment):
    '''Edit homework comment.'''
    try:
        comment = HomeworkComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    if not (request.user.is_teacher or comment.author.pk == request.user.pk):
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'homework': comment.homework,
            'content': request.POST.get('content'),
            'author': comment.author
        }
        form = HomeworkCommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            page = request.POST.get('page', '')
            return redirect(f'/homework/{comment.homework.pk}?page={page}#comment{comment.pk}')
        else:
            context = {
                'comment': comment,
                'errors': form.errors
            }
            return render(request, "homeworks/edit_homework_comment.html", context)
    else:
        return render(request, "homeworks/edit_homework_comment.html", {'comment': comment})


@is_teacher
def delete_homework_comment(request, comment):
    '''Delete homework comment.'''
    try:
        comment = HomeworkComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    homework = comment.homework
    comment.delete()
    return redirect(f'/homework/{homework.pk}')


# Helper for the below two
@is_teacher
def set_homework_comment_star(request, comment, status):
    '''Set a star to a homework comment.'''
    try:
        comment = HomeworkComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('missing')
    comment.starred = status
    comment.save()
    page = request.GET.get('page', '')
    return redirect(f'/homework/{comment.homework.pk}?page={page}#comment{comment.pk}')

@is_teacher
def add_homework_comment_star(request, comment):
    '''Add star to a homework comment.'''
    return set_homework_comment_star(request, comment, True)

@is_teacher
def remove_homework_comment_star(request, comment):
    '''Remove a star from a homework comment.'''
    return set_homework_comment_star(request, comment, False)
