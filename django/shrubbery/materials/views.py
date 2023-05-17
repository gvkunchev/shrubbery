from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from shrubbery.view_decorators import is_teacher

from .models import Material
from .forms import MaterialForm


def materials(request):
    '''Materials page.'''
    return render(request, "materials.html", {'materials': Material.objects.all()})


@is_teacher
def lectures(request):
    '''Lectures overview.'''
    return render(request, "lectures/lectures.html", {'lectures': Material.objects.all()})


@is_teacher
def lecture(request, lecture):
    '''Edit a single lecture.'''
    try:
        lecture_obj = Material.objects.get(pk=lecture)
    except ObjectDoesNotExist:
        return redirect('shrubbery:missing')
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = MaterialForm(request.POST, request.FILES, instance=lecture_obj)
            if form.is_valid():
                form.save()
                context = {
                    'lecture': lecture_obj,
                    'info': 'Успешно редактира лекция'
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
                'info': 'Успешно изтри лекция'
            }
            return render(request, "lectures/lectures.html", context)
        else:
            return redirect('shrubbery:missing')
    else:
        return render(request, "lectures/lecture.html", {'lecture': lecture_obj})


@is_teacher
def add_lecture(request):
    '''Add new lecture.'''
    form = MaterialForm(request.POST, request.FILES)
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
