from django import template

register = template.Library()

from homeworksolutions.models import HomeworkSolution
from homeworksolutions.models import HomeworkSolutionHistoryInlineComment


@register.simple_tag()
def create_list(*args):
    return args

@register.simple_tag(name='zip')
def zip_many(*args):
    return list(zip(*args))

@register.simple_tag()
def get_homework_results(data, homework):
    key = f'homework_{homework.pk}'
    return data.get(key, '-')

@register.simple_tag()
def get_exam_results(data, exam):
    key = f'exam_{exam.pk}'
    return data.get(key, '-')

@register.filter()
def activate_link(request_path, url):
    """Determine whether to active a link in the navbar ot not."""
    if url == '/':
        return request_path == '/'
    return url.rstrip('s') in request_path


@register.filter()
def solution_from(homework, user):
    """Get the solution to a homework from a user."""
    try:
        return HomeworkSolution.objects.get(author=user, homework=homework)
    except:
        return False


@register.filter()
def inline_comments_from_history(history):
    """Get the inline comments from a history."""
    return HomeworkSolutionHistoryInlineComment.objects.filter(history=history)

@register.filter(name='times') 
def times(number):
    """Range from integer."""
    return range(number)

@register.filter(name='abs')
def abs_filter(value):
    return abs(value)