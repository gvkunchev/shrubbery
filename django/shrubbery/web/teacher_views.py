from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from users.forms import AddStudentForm, EditStudentForm, EditTeacherForm
from news.forms import AddNewsArticleForm
from news.models import NewsArticle
from users.models import Student, Teacher

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
                'errors': form.errors,
                'info': 'Успешно редактирахте студент'
            }
            return render(request, "participants/participant.html", context)
        elif 'delete' in request.POST:
            participant_obj.delete()
            context = {
                'participants': Student.objects.all(),
                'info': 'Успешно изтрихте студент'
            }
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
            teacher_obj.delete()
            context = {
                'team': Teacher.objects.all(),
                'info': 'Успешно изтрихте учител'
            }
            return render(request, "team/team.html", context)
        else:
            return redirect('web:missing')
    else:
        return render(request, "team/team_member.html", {'teacher': teacher_obj})


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
