from django.shortcuts import render


def info(request):
    '''Information pages content.'''
    return render(request, "info/info.html")


def info_showdown(request):
    '''Showdown syntax information.'''
    return render(request, "info/showdown.html")


def info_code(request):
    '''Code submit information.'''
    return render(request, "info/code.html")
