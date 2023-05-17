from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import PasswordChangeForm

from shrubbery.view_decorators import is_teacher

from .forms import (EditUserForm, PasswordSetForm,
                    RegisterStudent, EditStudentForm,
                    AddStudentForm, EditTeacherForm,
                    AddTeacherForm)
from .emails import send_activation_email
from .models import User, Student, Teacher
from .tokens import account_activation_token


# Authorization views

def login_(request):
    '''Login page.'''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            return render(request, "auth/login.html",
                          {'errors': 'unauthorized'})
        else:
            login(request, user)
            try:
                return redirect(request.GET['next'])
            except KeyError:
                return redirect('/')
    else:
        return render(request, "auth/login.html")


def logout_(request):
    '''Logut.'''
    logout(request)
    return redirect('/')


def activate(request):
    """Activate an account."""
    if request.method == 'GET':
        try:
            uidb64 = request.GET['uidb64']
            token = request.GET['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, 'auth/activated.html', {'correct': True})
        else:
            return render(request, 'auth/activated.html', {'correct': False})
    else:
        try:
            uidb64 = request.POST['uidb64']
            token = request.POST['token']
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            print(request.POST['uidb64'])
            print(request.POST['token'])
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = PasswordSetForm(user, request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                login(request, user)
                update_session_auth_hash(request, user)
                return render(request, "home.html", {'welcome': True})
            else:
                context = {
                    'correct': True,
                    'errors': form.errors
                }
                return render(request, 'auth/activated.html', context)
        else:
            return render(request, 'auth/activated.html', {'correct': False})


def register(request):
    """Student form for registering their email."""
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            fn = request.POST['fn'].strip()
            user = Student.objects.get(first_name=first_name, last_name=last_name, fn=fn)
        except Exception as e:
            context = {
                'error': 'Липсваш от списъка.'
            }
            return render(request, "auth/register.html", context)
        if user.is_active:
            context = {
                'error': 'Вече си регистриран.'
            }
            return render(request, "auth/register.html", context)
        form = RegisterStudent(request.POST, instance=user)
        if form.is_valid():
            form.save()
            send_activation_email(request, user)
            context = {
                'info': 'Изпратен е имейл за активация.'
            }
        else:
            context = {
                'errors': form.errors
            }
        return render(request, "auth/register.html", context)
    else:
        return render(request, "auth/register.html")


# User own settings

@login_required
def settings(request):
    '''Profile settings.'''
    if request.method == 'POST':
        if 'personal_info' in request.POST:
            # If these checks are missing, users can upload new images, but the
            # image is not processed. Image uploda happens before validation so
            # they can upload files without any validation being done.
            # There is already front-end validation that requires inputing these fields.
            # This is just in case.
            if 'first_name' not in request.POST or request.POST['first_name'] == '':
                return redirect('missing')
            if 'last_name' not in request.POST or request.POST['last_name'] == '':
                return redirect('missing')
            form = EditUserForm(request.POST, request.FILES, instance=request.user)
            context = {}
            if form.is_valid():
                form.save()
                context = {
                    'settings_info': 'Настройките са запазени'
                }
                if request.POST.get('image_remove'):
                    request.user.image = None
                    request.user.save()
            else:
                context = {
                    'errors': form.errors
                }
            return render(request, "settings.html", context)
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                context = {
                    'password_info': 'Паролата е сменена'
                }
            else:
                context = {
                    'errors': form.errors
                }
            return render(request, "settings.html", context)
        else:
            return redirect('missing')
    else:
        return render(request, "settings.html")


# Public student views

def students(request):
    '''Students page.'''
    all_students = Student.objects.filter(is_active=True)
    paginator = Paginator(all_students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "students/students.html", {'students': page_obj})


def student(request, student):
    '''Single student page.'''
    try:
        student = Student.objects.get(pk=student)
        if not student.is_active:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "students/student.html", {'student': student})


# Public teacher views

def teachers(request):
    '''Teachers page.'''
    teachers = Teacher.objects.all().filter(is_active=True)
    return render(request, "teachers/teachers.html", {'teachers': teachers})


def teacher(request, teacher):
    '''Single teacher page.'''
    try:
        teacher = Teacher.objects.get(pk=teacher)
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "teachers/teacher.html", {'teacher': teacher})


# Administration student views

@is_teacher
def participants(request):
    '''List of participants.'''
    return render(request, "participants/participants.html", {'participants': Student.objects.all()})


@is_teacher
def participant(request, participant):
    '''Edit a single participant.'''
    try:
        participant_obj = Student.objects.get(pk=participant)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditStudentForm(request.POST, instance=participant_obj)
            if form.is_valid():
                form.save()
                context = {
                    'participant': participant_obj,
                    'info': 'Успешно редактира студент'
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
                    'info': 'Успешно изтри студент'
                }
                # Keeping the POST data will refill
                # the inputs with it, which is useful on
                # error, but should not be done on success
                request.POST = {}
                return render(request, "participants/participants.html", context)
        else:
            return redirect('missing')
    else:
        return render(request, "participants/participant.html", {'participant': participant_obj})


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


# Administration teacher views

@is_teacher
def team(request):
    '''Team of teachers view.'''
    return render(request, "team/team.html", {'team': Teacher.objects.all()})


@is_teacher
def team_member(request, teacher):
    '''Edit a single teacher.'''
    try:
        teacher_obj = Teacher.objects.get(pk=teacher)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = EditTeacherForm(request.POST, instance=teacher_obj)
            if form.is_valid():
                form.save()
            context = {
                'teacher': teacher_obj,
                'errors': form.errors,
                'info': 'Успешно редактира учител'
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
                    'team': Teacher.objects.all(),
                    'info': 'Успешно изтри учител'
                }
                # Keeping the POST data will refill
                # the inputs with it, which is useful on
                # error, but should not be done on success
                request.POST = {}
                return render(request, "team/team.html", context)
        else:
            return redirect('missing')
    else:
        return render(request, "team/team_member.html", {'teacher': teacher_obj})


@is_teacher
def add_team_member(request):
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
