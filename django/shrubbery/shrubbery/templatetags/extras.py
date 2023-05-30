import six
from django import template
from django.template.base import Node
from django.utils.functional import keep_lazy

register = template.Library()

from homeworksolutions.models import HomeworkSolution
from homeworksolutions.models import HomeworkSolutionHistoryInlineComment
from challengesolutions.models import ChallengeSolution


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
def get_challenge_results(data, challenge):
    key = f'challenge_{challenge.pk}'
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
def homework_solution_from(homework, user):
    """Get the solution to a homework from a user."""
    try:
        return HomeworkSolution.objects.get(author=user, homework=homework)
    except:
        return False

@register.filter()
def challenge_solution_from(challenge, user):
    """Get the solution to a challenge from a user."""
    try:
        return ChallengeSolution.objects.get(author=user, homechallengework=challenge)
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

@register.tag
def linebreakless(parser, token):
    nodelist = parser.parse(('endlinebreakless',))
    parser.delete_first_token()
    return LinebreaklessNode(nodelist)


class LinebreaklessNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        strip_line_breaks = keep_lazy(six.text_type)(lambda x: x.replace('\n', '').replace('\r', ''))
        return strip_line_breaks(self.nodelist.render(context).strip())
