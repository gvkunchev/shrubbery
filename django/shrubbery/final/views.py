import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shrubbery.view_decorators import is_teacher, is_student
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.apps import apps

from .models import FinalScheduleSlot, FinalExchange
from users.models import Student
from .forms import FinalScheduleSlotForm


@is_teacher
def schedule_editor(request):
    """Final schedule editor."""
    slots = FinalScheduleSlot.objects.all()
    return render(request, "final/schedule_editor.html", {'slots': slots})


@is_teacher
#@login_required # TODO: Put back if you want to show the schedule to students and remove the line above
def schedule(request):
    """Final schedule."""
    slots = FinalScheduleSlot.objects.all()
    context = {'slots': slots}
    if request.user.is_student:
        student = Student.objects.get(pk=request.user.pk)
        if not student.finalscheduleslot_set.values():
            context['not_in_schedule'] = True
        else:
            context['enable_find_me'] = True
            context['my_slot'] = student.finalscheduleslot_set.get()
        exchange_requester = FinalExchange.objects.filter(requester=student)
        exchange_confirmer = FinalExchange.objects.filter(confirmer=student)
        context['exchange_requester'] = exchange_requester
        context['exchange_confirmer'] = exchange_confirmer
    return render(request, "final/schedule.html", context)


@is_teacher
def add_slot(request):
    """Add a new slot."""
    form = FinalScheduleSlotForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/final/schedule_editor')
    else:
        slots = FinalScheduleSlot.objects.all()
        return render(request, "final/schedule_editor.html",
                      {'slots': slots, 'errors': form.errors})


@is_teacher
def add_slots(request):
    '''Add slots from a file.'''
    try:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
    except:
        context = {
            'slots': FinalScheduleSlot.objects.all(),
            'errors': {'csv': 'Грешка при обработка на файла.'}
        }
        return render(request, "final/schedule_editor.html", context)
    errors = []
    counter = 0
    for i, line in enumerate(lines):
        if not line:
            continue
        try:
            start, end, *students = line.split(',')
            start = start.strip()
            end = end.strip()
            start = datetime.datetime.strptime(start, '%d.%m.%Y %H:%M')
            end = datetime.datetime.strptime(end, '%d.%m.%Y %H:%M')
            students = list(map(str.strip, students))
            data = {
                'start': start,
                'end': end
            }
            form = FinalScheduleSlotForm(data)
            if form.is_valid():
                slot = form.save()
                for student in students:
                    if not student:
                        continue
                    try:
                        student = Student.objects.get(fn=student)
                    except ObjectDoesNotExist:
                        errors.append((i, line, f'Студент с ФН={student} не е намерен.'))
                        continue
                    if student.finalscheduleslot_set.values():
                        errors.append((i, line, f'{student.full_name} вече е в слот и не може да бъде добавен в този слот.'))
                    else:
                        slot.students.add(student)
                counter += 1
            else:
                errors.append((i, line, str(form.errors)))
        except Exception as e:
            errors.append((i, line, f'Грешка при обработка на реда: {e}'))
    context = {
        'slots': FinalScheduleSlot.objects.all(),
        'errors': {'csv_list': errors},
        'info': f'Добавени бяха {counter} слота.'
    }
    return render(request, "final/schedule_editor.html", context)


@is_teacher
def remove_slot(request, slot):
    """Remove a slot."""
    try:
        slot = FinalScheduleSlot.objects.get(pk=slot)
        slot.delete()
    except ObjectDoesNotExist:
        return redirect('missing')
    return redirect('/final/schedule_editor')


@is_teacher
def edit_slot(request, slot):
    """Edit a slot."""
    try:
        slot = FinalScheduleSlot.objects.get(pk=slot)
    except ObjectDoesNotExist:
        return redirect('missing')
    students = Student.objects.all()
    if request.method == 'GET':
        return render(request, "final/edit_slot.html", {'slot': slot, 'students': students})
    else:
        form = FinalScheduleSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect('/final/schedule_editor')
        else:
            return render(request, "final/edit_slot.html", {'slot': slot, 'students': students,
                                                            'errors': form.errors})


@is_teacher
def remove_student(request, slot, student):
    """Remove student from a slot."""
    try:
        slot = FinalScheduleSlot.objects.get(pk=slot)
        student = Student.objects.get(pk=student)
    except ObjectDoesNotExist:
        return redirect('missing')
    slot.students.remove(student)
    return redirect(f'/final/slot/edit/{slot.pk}')


@is_teacher
def add_student(request, slot):
    """Add student to a slot."""
    try:
        slot = FinalScheduleSlot.objects.get(pk=slot)
        if request.POST.get('student') == '0':
            return redirect(f'/final/slot/edit/{slot.pk}')
        student = Student.objects.get(pk=request.POST.get('student'))
        if student.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Student already in a slot.')
    except (ObjectDoesNotExist, KeyError):
        return redirect('missing')
    slot.students.add(student)
    return redirect(f'/final/slot/edit/{slot.pk}')


@is_student
def request_exchange(request, student):
    """Request exchange with a student."""
    try:
        user = Student.objects.get(pk=request.user.pk)
        student = Student.objects.get(pk=student)
        # Ensure requester have not requested another exchange
        if user.exchange_requests.values():
            raise ObjectDoesNotExist('User already requested an exchange.')
        # Ensure both students are already in a slot
        if not user.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Logged in student is not in a slot.')
        if not student.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Requested user is not in a slot.')
        # Ensure students are not in the same slot already
        if user.finalscheduleslot_set.get() == student.finalscheduleslot_set.get():
            raise ObjectDoesNotExist('Users are already in the same slot.')
        exchange = FinalExchange.objects.create(requester=user, confirmer=student)
        exchange.save()
        return redirect('/final/schedule')
    except ObjectDoesNotExist:
        return redirect('missing')


@is_student
def cancel_exchange(request, student):
    """Cancel exchange request."""
    try:
        user = Student.objects.get(pk=request.user.pk)
        student = Student.objects.get(pk=student)
        exchange = user.exchange_requests.get()
        # Ensure the requested student is really the confirmer
        if exchange.confirmer.pk != student.pk:
            raise ObjectDoesNotExist('Exchange confirmed is not this student.')
        # Ensure both students are already in a slot
        if not user.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Logged in student is not in a slot.')
        if not student.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Requested user is not in a slot.')
        exchange.delete()
        return redirect('/final/schedule')
    except ObjectDoesNotExist:
        return redirect('missing')


@is_student
def confirm_exchange(request, student):
    """Confirm exchange with a student."""
    try:
        user = Student.objects.get(pk=request.user.pk)
        student = Student.objects.get(pk=student)
        exchange_request = student.exchange_requests.get()
        exchange_confirmation = user.exchange_confirmations.get()
        # Ensure the requests match
        if exchange_request.pk != exchange_confirmation.pk:
            raise ObjectDoesNotExist('Exchange confirmed is not this student.')
        # Ensure both students are already in a slot
        if not user.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Logged in student is not in a slot.')
        if not student.finalscheduleslot_set.values():
            raise ObjectDoesNotExist('Requested user is not in a slot.')
        # Ensure students are not in the same slot already
        if user.finalscheduleslot_set.get() == student.finalscheduleslot_set.get():
            raise ObjectDoesNotExist('Users are already in the same slot.')
        user_slot = user.finalscheduleslot_set.get()
        student_slot = student.finalscheduleslot_set.get()
        user_slot.students.remove(user)
        user_slot.students.add(student)
        student_slot.students.remove(student)
        student_slot.students.add(user)
        exchange_request.delete()
        action = apps.get_model('activity.Action').objects.create(author=user,
                                                                  link=f'final/schedule#student_{student.pk}',
                                                                  date=timezone.now(),
                                                                  type='FSC')
        action.save()
        return redirect('/final/schedule')
    except ObjectDoesNotExist:
        return redirect('missing')
