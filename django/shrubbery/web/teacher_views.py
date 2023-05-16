from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from users.forms import (AddStudentForm, EditStudentForm,
                         EditTeacherForm, AddTeacherForm)
from materials.forms import EditMaterialForm
from news.forms import AddNewsArticleForm
from news.models import NewsArticle
from users.models import Student, Teacher
from users.emails import send_activation_email
from materials.models import Material
from forum.models import Forum, ForumComment
from forum.forms import ForumForm

from .view_decorators import is_teacher


@is_teacher
def participants(request):
    '''List of participants.'''
    return render(request, "participants/participants.html", {'participants': Student.objects.all()})


@is_teacher
def team(request):
    '''Team of teachers view.'''
    return render(request, "team/team.html", {'team': Teacher.objects.all()})


@is_teacher
def lectures(request):
    '''Lectures overview.'''
    return render(request, "lectures/lectures.html", {'lectures': Material.objects.all()})


@is_teacher
def add_participant(request):
    '''Add new participant.'''
    form = AddStudentForm(request.POST)
    if form.is_valid():
        student = form.save(commit=False)
        student.email = f'{student.fn}@notset.com'
        student.is_active = False
        student.save()
        context = {
            'participants': Student.objects.all(),
            'info': 'Студентът е добавен'
        }
        # Keeping the POST data will refill
        # the inputs with it, which is useful on
        # error, but should not be done on success
        request.POST = {}
        return render(request, "participants/participants.html", context)
    else:
        context = {
            'participants': Student.objects.all(),
            'errors': form.errors
        }
        return render(request, "participants/participants.html", context)


@is_teacher
def add_participants(request):
    '''Add new participants from a file.'''
    try:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
    except:
        context = {
            'participants': Student.objects.all(),
            'errors': {'csv': 'Грешка при обработка на файла.'}
        }
        return render(request, "participants/participants.html", context)
    errors = []
    counter = 0
    for i, line in enumerate(lines):
        if not line:
            continue
        try:
            first_name, last_name, fn = line.split(',')
            first_name = first_name.strip()
            last_name = last_name.strip()
            fn = fn.strip()
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'fn': fn
            }
            form = AddStudentForm(data)
            if form.is_valid():
                student = form.save(commit=False)
                student.email = f'{student.fn}@notset.com'
                student.is_active = False
                student.save()
                counter += 1
            else:
                errors.append((i, line, str(form.errors)))
        except Exception as e:
            errors.append((i, line, f'Грешка при обработка на реда: {e}'))
    context = {
        'participants': Student.objects.all(),
        'errors': {'csv_list': errors},
        'info': f'Добавени бяха {counter} студента.'
    }
    return render(request, "participants/participants.html", context)


@is_teacher
def participant(request, participant):
    '''Edit a single participant.'''
    try:
        participant_obj = Student.objects.get(pk=participant)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditStudentForm(request.POST, instance=participant_obj)
            if form.is_valid():
                form.save()
                context = {
                    'participant': participant_obj,
                    'info': 'Успешно редактирахте студент'
                }
            else:
                context = {
                    'participant': participant_obj,
                    'errors': form.errors
                }
            return render(request, "participants/participant.html", context)
        elif 'delete' in request.POST:
            if participant_obj.is_active:
                context = {
                    'participant': participant_obj,
                    'error': ('Не можеш да изтриеш активен студент. '
                              'Използвай конзолата, за да го деактивираш.')
                }
                return render(request, "participants/participant.html", context)
            else:
                participant_obj.delete()
                context = {
                    'participants': Student.objects.all(),
                    'info': 'Успешно изтрихте студент'
                }
                # Keeping the POST data will refill
                # the inputs with it, which is useful on
                # error, but should not be done on success
                request.POST = {}
                return render(request, "participants/participants.html", context)
        else:
            return redirect('web:missing')
    else:
        return render(request, "participants/participant.html", {'participant': participant_obj})


@is_teacher
def team_member(request, teacher):
    '''Edit a single teacher.'''
    try:
        teacher_obj = Teacher.objects.get(pk=teacher)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditTeacherForm(request.POST, instance=teacher_obj)
            if form.is_valid():
                form.save()
            context = {
                'teacher': teacher_obj,
                'errors': form.errors,
                'info': 'Успешно редактирахте учител'
            }
            return render(request, "team/team_member.html", context)
        elif 'delete' in request.POST:
            if teacher_obj.is_active:
                context = {
                    'participant': teacher_obj,
                    'error': ('Не можеш да изтриеш активен учител. '
                              'Използвай конзолата, за да го деактивираш.')
                }
                return render(request, "team/team_member.html", context)
            else:
                teacher_obj.delete()
                context = {
                    'team': Student.objects.all(),
                    'info': 'Успешно изтрихте учител'
                }
                # Keeping the POST data will refill
                # the inputs with it, which is useful on
                # error, but should not be done on success
                request.POST = {}
                return render(request, "team/team.html", context)
        else:
            return redirect('web:missing')
    else:
        return render(request, "team/team_member.html", {'teacher': teacher_obj})


@is_teacher
def add_teacher(request):
    '''Add new teacher.'''
    form = AddTeacherForm(request.POST)
    if form.is_valid():
        teacher = form.save(commit=False)
        teacher.is_active = False
        teacher.save()
        context = {
            'team': Teacher.objects.all(),
            'info': 'Учителят е добавен. Изпратен е имейл за активация.'
        }
        send_activation_email(request, teacher)
        # Keeping the POST data will refill
        # the inputs with it, which is useful on
        # error, but should not be done on success
        request.POST = {}
        return render(request, "team/team.html", context)
    else:
        context = {
            'team': Teacher.objects.all(),
            'errors': form.errors
        }
        return render(request, "team/team.html", context)


@is_teacher
def add_news_article(request):
    '''Add news article.'''
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = AddNewsArticleForm(data)
        if form.is_valid():
            form.save()
            return redirect('web:news')
        else:
            return render(request, "news/add_news_article.html", {'errors': form.errors})
    else:
        return render(request, "news/add_news_article.html")


@is_teacher
def edit_news_article(request, article):
    '''Edit news article.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = AddNewsArticleForm(data, instance=article)
        if form.is_valid():
            form.save()
            return redirect(f'/news/{article.pk}')
        else:
            context = {
                'article': article,
                'errors': form.errors
            }
            return render(request, "news/edit_news_article.html", context)
    else:
        return render(request, "news/edit_news_article.html", {'article': article})


@is_teacher
def delete_news_article(request, article):
    '''Delete news article.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    article.delete()
    return redirect('web:news')


@is_teacher
def lecture(request, lecture):
    '''Edit a single lecture.'''
    try:
        lecture_obj = Material.objects.get(pk=lecture)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditMaterialForm(request.POST, request.FILES, instance=lecture_obj)
            if form.is_valid():
                form.save()
                context = {
                    'lecture': lecture_obj,
                    'info': 'Успешно редактирахте лекция'
                }
            else:
                print(form.errors)
                context = {
                    'lecture': lecture_obj,
                    'errors': form.errors,
                }
            return render(request, "lectures/lecture.html", context)
        elif 'delete' in request.POST:
            lecture_obj.delete()
            context = {
                'lectures': Material.objects.all(),
                'info': 'Успешно изтрихте лекция'
            }
            return render(request, "lectures/lectures.html", context)
        else:
            return redirect('web:missing')
    else:
        return render(request, "lectures/lecture.html", {'lecture': lecture_obj})


@is_teacher
def add_lecture(request):
    '''Add new lecture.'''
    form = EditMaterialForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        context = {
            'lectures': Material.objects.all(),
            'info': 'Лекцията е добавена'
        }
        # Keeping the POST data will refill
        # the inputs with it, which is useful on
        # error, but should not be done on success
        request.POST = {}
        return render(request, "lectures/lectures.html", context)
    else:
        context = {
            'lectures': Material.objects.all(),
            'errors': form.errors
        }
        return render(request, "lectures/lectures.html", context)


@is_teacher
def edit_forum(request, forum):
    '''Edit forum.'''
    try:
        forum = Forum.objects.get(pk=forum)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.user
        }
        form = ForumForm(data, instance=forum)
        if form.is_valid():
            form.save()
            return redirect(f'/forum/{forum.pk}')
        else:
            context = {
                'forum': forum,
                'errors': form.errors
            }
            return render(request, "forums/edit_forum.html", context)
    else:
        return render(request, "forums/edit_forum.html", {'forum': forum})


@is_teacher
def delete_forum(request, forum):
    '''Delete forum.'''
    try:
        forum = Forum.objects.get(pk=forum)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    forum.delete()
    return redirect('web:forums')


@is_teacher
def delete_forum_comment(request, comment):
    '''Delete forum.'''
    try:
        comment = ForumComment.objects.get(pk=comment)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    forum = comment.forum
    comment.delete()
    return redirect(f'/forum/{forum.pk}')
