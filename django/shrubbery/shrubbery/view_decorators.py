from django.shortcuts import redirect


def is_teacher(function):
    def wrapper(request, *args, **kw):
        if not request.user:
            return redirect('missing')
        if not request.user.is_authenticated:
            return redirect('missing')
        if not request.user.is_teacher:
            return redirect('missing')
        return function(request, *args, **kw)
    return wrapper


def is_student(function):
    def wrapper(request, *args, **kw):
        if not request.user:
            return redirect('missing')
        if not request.user.is_authenticated:
            return redirect('missing')
        if not request.user.is_student:
            return redirect('missing')
        return function(request, *args, **kw)
    return wrapper
