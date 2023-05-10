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
        return redirect('web:participants')
    else:
        context = {
            'participants': Student.objects.all(),
            'errors': form.errors
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
                'errors': form.errors
            }
            return render(request, "participants/participant.html", context)
        else:
            participant_obj.delete()
            return redirect('web:participants')
    else:
        return render(request, "participants/participant.html", {'participant': participant_obj})
