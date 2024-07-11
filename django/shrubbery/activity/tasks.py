import os

from django.utils import timezone
from django.template.loader import render_to_string

from celery import shared_task

from shrubbery.email import Emailer
from users.models import Student
from homeworksolutions.models import HomeworkSolution
from challengesolutions.models import ChallengeSolution
from points.getters import get_point_summary

BACKUP_POINTS_EMAIL = 'gvkunchev@gmail.com'

EMAILER = Emailer()
if os.environ.get('SHRUBBERY_ENV') == 'prd':
    DOMAIN = 'https://2024.py-fmi.org'
else:
    DOMAIN = 'http://localhost:8080'


@shared_task(name="alert_for_new_solution_comments")
def alert_for_new_solution_comments(*args, **kwargs):
    """Send alerts for new comments on solutions."""
    for student in Student.objects.filter(is_active=True, email_notification_solution_comments=True):
        homeworks = HomeworkSolution.objects.filter(author=student)
        challenges = ChallengeSolution.objects.filter(author=student)
        comments = {
            'homework': {
                'overall': [],
                'inline': [],
            },
            'challenge': {
                'overall': [],
                'inline': [],
            }
        }
        for homework in homeworks:
            comments['homework']['overall'] += homework.homeworksolutioncomment_set.all()
            comments['homework']['inline'] += homework.homeworksolutioninlinecomment_set.all()
        for challenge in challenges:
            comments['challenge']['overall'] += challenge.challengesolutioncomment_set.all()
            comments['challenge']['inline'] += challenge.challengesolutioninlinecomment_set.all()
        new_comments = []
        for task_type in comments.keys():
            for comment_type in comments[task_type].keys():
                for comment in comments[task_type][comment_type]:
                    if comment.author.pk == student.pk:
                        continue # Student's own comment
                    if timezone.now() - comment.date < timezone.timedelta(minutes=60):
                        new_comments.append({
                            'task_type': task_type,
                            'solution': comment.solution,
                            'comment_type': comment_type,
                            'comment': comment
                        })
                        if task_type == 'homework':
                            new_comments[-1].update({'task': comment.solution.homework})
                        else:
                            new_comments[-1].update({'task': comment.solution.challenge})
        if len(new_comments):
            context = {
                'domain':DOMAIN,
                'comments': new_comments
            }
            EMAILER.send_email([student.email], 'Python @ ФМИ - Нов коментар по решение',
                               render_to_string('emails/solution_comment_created.html', context))


@shared_task(name="backup_points")
def backup_points(*args, **kwargs):
    """Backup the points via email send."""
    return True # Disabled due to lack of need for this at the moment
    points = {}
    for student in Student.objects.filter(is_active=True):
        points[student.fn] = {
            'name': student.full_name,
            'points': get_point_summary(student)
        }
    EMAILER.send_email([BACKUP_POINTS_EMAIL], 'Python @ ФМИ - Points backup', str(points))
