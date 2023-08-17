from django.shortcuts import render

from users.models import Teacher

def info(request):
    '''Information pages content.'''
    context = {
        'teachers': map(lambda x: x.email, Teacher.objects.filter(is_active=True))
    }
    return render(request, "info/info.html", context)


def info_showdown(request):
    '''Showdown syntax information.'''
    return render(request, "info/showdown.html")


def info_code(request):
    '''Code submit information.'''
    return render(request, "info/code.html")
