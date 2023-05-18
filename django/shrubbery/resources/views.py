from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from shrubbery.view_decorators import is_teacher

from .models import Resource
from .forms import ResourceForm


@is_teacher
def resources(request):
    '''Resources page.'''
    return render(request, "resources.html", {'resources': Resource.objects.all()})


@is_teacher
def add_resource(request):
    '''Add new resource.'''
    form = ResourceForm(request.POST, request.FILES)
    if form.is_valid():
        resource = form.save()
        context = {
            'resources': Resource.objects.all(),
            'resource': resource,
            'info': 'Ресурсът е добавен'
        }
        return render(request, "resources.html", context)
    else:
        context = {
            'lectures': Resource.objects.all(),
            'errors': form.errors
        }
        return render(request, "resources.html", context)


@is_teacher
def remove_resources(request):
    '''Remove resources.'''
    resources = []
    try:
        for field in request.POST:
            if field.startswith('resource_'):
                pk = field.replace('resource_', '')
                resources.append(Resource.objects.get(pk=pk))
    except ObjectDoesNotExist:
        return redirect('missing')
    for resource in resources:
        resource.delete()
    context = {
        'resources': Resource.objects.all()
    }
    if len(resources):
        context['info'] = 'Успешно изтри ресурсите.'
    return render(request, "resources.html", context)
