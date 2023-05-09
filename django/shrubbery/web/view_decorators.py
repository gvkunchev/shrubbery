from django.shortcuts import redirect


def is_teacher(function):
    def wrapper(request, *args, **kw):
        if not request.user:
            return redirect('web:missing')
        if not request.user.is_authenticated:
            return redirect('web:missing')
        if not request.user.is_teacher:
            return redirect('web:missing')
        return function(request, *args, **kw)
    return wrapper
