from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from users.forms import AddStudentForm, EditStudentForm
from users.models import Student

from .view_decorators import is_teacher


@is_teacher
def participants(request):
    '''List of participants.'''
    return render(request, "participants/participants.html", {'participants': Student.objects.all()})


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
        return render(request, "participants/participant.html", {'participant': participant_obj})
