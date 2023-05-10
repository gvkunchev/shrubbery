from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from news.models import NewsArticle
from materials.models import Material
from users.models import Student, Teacher


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "backbone/missing.html")


def home(request):
    '''Home page.'''
    return render(request, "home.html", {'news': NewsArticle.objects.all()})


def materials(request):
    '''Materials page.'''
    return render(request, "materials.html", {'materials': Material.objects.all()})


def students(request):
    '''Students page.'''
    return render(request, "students/students.html", {'students': Student.objects.filter(is_active=True)})


def student(request, student):
    '''Single student page.'''
    try:
        student = Student.objects.get(pk=student)
        if not student.is_active:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "students/student.html", {'student': student})


def teachers(request):
    '''Teachers page.'''
    return render(request, "teachers/teachers.html", {'teachers': Teacher.objects.all()})


def teacher(request, teacher):
    '''Single teacher page.'''
    try:
        teacher = Teacher.objects.get(pk=teacher)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "teachers/teacher.html", {'teacher': teacher})


def news(request):
    '''News page.'''
    return render(request, "news/news.html", {'news': NewsArticle.objects.all()})


def news_article(request, article):
    '''News article page.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "news/news_article.html", {'article': article})
