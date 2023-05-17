from django.shortcuts import redirect


def is_teacher(function):
    def wrapper(request, *args, **kw):
        if not request.user:
            return redirect('shrubbery:missing')
        if not request.user.is_authenticated:
            return redirect('shrubbery:missing')
        if not request.user.is_teacher:
            return redirect('shrubbery:missing')
        return function(request, *args, **kw)
    return wrapper
