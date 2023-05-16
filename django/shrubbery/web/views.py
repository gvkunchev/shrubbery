from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from news.models import NewsArticle
from materials.models import Material
from users.models import Student, Teacher
from forum.models import Forum


def missing(request, exception=None):
    '''Not found page.'''
    return render(request, "backbone/missing.html")


def home(request):
    '''Home page.'''
    MAX_NEWS = 5
    return render(request, "home.html", {'news': NewsArticle.objects.all()[:MAX_NEWS]})


def materials(request):
    '''Materials page.'''
    return render(request, "materials.html", {'materials': Material.objects.all()})


def forums(request):
    '''Forums page.'''
    return render(request, "forums/forums.html", {'forums': Forum.objects.all()})


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
        return redirect('web:missing')
    return render(request, "students/student.html", {'student': student})


def teachers(request):
    '''Teachers page.'''
    teachers = Teacher.objects.all().filter(is_active=True)
    return render(request, "teachers/teachers.html", {'teachers': teachers})


def teacher(request, teacher):
    '''Single teacher page.'''
    try:
        teacher = Teacher.objects.get(pk=teacher)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "teachers/teacher.html", {'teacher': teacher})


def news(request):
    '''News page.'''
    all_news = NewsArticle.objects.all()
    paginator = Paginator(all_news, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "news/news.html", {'news': page_obj})


def news_article(request, article):
    '''News article page.'''
    try:
        article = NewsArticle.objects.get(pk=article)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "news/news_article.html", {'article': article})

def forum(request, forum):
    '''Forum article page.'''
    try:
        forum = Forum.objects.get(pk=forum)
        paginator = Paginator(forum.comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except ObjectDoesNotExist:
        return redirect('web:missing')
    return render(request, "forums/forum.html", {'forum': forum, 'comments': page_obj})

