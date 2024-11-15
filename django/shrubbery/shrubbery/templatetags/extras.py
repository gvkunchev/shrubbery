import six
from django.conf import settings
from django import template
from django.template.base import Node
from django.utils.functional import keep_lazy
from users.models import User
register = template.Library()

from homeworksolutions.models import HomeworkSolution
from homeworksolutions.models import HomeworkSolutionHistoryInlineComment
from challengesolutions.models import ChallengeSolution, ChallengeSolutionHistoryInlineComment


@register.simple_tag()
def show_final_schedule(*args):
    return settings.SHOW_FINAL_SCHEDULE

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
def is_subscribed_to(user, task):
    """Check if teacher is subscribed to a homework/challenge."""
    return user.pk in map(lambda x: x.pk, task.subscribers.all())

@register.filter()
def calculate_filter(current_vars, filter):
    """Calculate filter variables for a link."""
    resulting_vars = list(current_vars.keys())
    if filter in resulting_vars:
        resulting_vars.remove(filter)
    else:
        resulting_vars.append(filter)
    return f"?{'&'.join(resulting_vars)}"


@register.filter()
def overwrite_to_history(link):
    """Remove ID at the end of link and put histoyr ID instead."""
    return f"{link.split('#')[0]}#history"


@register.filter()
def clean_github_profile(profile):
    """Remove link form GitHub profile (if any)."""
    return profile.split('/')[-1]


@register.filter()
def has_newer_version(task, date):
    """Check if a task has newer version than a date."""
    return task.has_history_after(date)

@register.filter()
def challenge_solution_from(challenge, user):
    """Get the solution to a challenge from a user."""
    try:
        return ChallengeSolution.objects.get(author=user, challenge=challenge)
    except:
        return False

@register.filter()
def inline_hw_comments_from_history(history):
    """Get the inline comments from a homework history."""
    return HomeworkSolutionHistoryInlineComment.objects.filter(history=history)

@register.filter()
def inline_c_comments_from_history(history):
    """Get the inline comments from a challenge history."""
    return ChallengeSolutionHistoryInlineComment.objects.filter(history=history)

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
