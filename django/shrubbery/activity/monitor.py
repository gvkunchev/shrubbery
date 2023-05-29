import os

from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from celery import shared_task

from users.models import User
from shrubbery.email import Emailer
from news.models import NewsArticle
from homeworks.models import Homework
from challenges.models import Challenge
from forum.models import Forum


EMAILER = Emailer()
if os.environ.get('SHRUBBERY_ENV') == 'prd':
    DOMAIN = 'https://shrubbery.onrender.com'
else:
    DOMAIN = 'http://localhost:8080'


def get_emails_from_queryset(queryset):
    """Get users' emails from a queryset."""
    return list(map(lambda user: user.email, queryset))


"""
Handlers
"""


@shared_task()
def send_email_newsarticle(instance):
    """Send email when a new article created."""
    queryset = User.objects.filter(is_active=True, is_superuser=False, email_notification_news=True)
    all_emails = get_emails_from_queryset(queryset)
    context = {
        'domain':DOMAIN,
        'id': instance.pk
    }
    EMAILER.send_email(all_emails, 'Python @ ФМИ - Новина',
                       render_to_string('emails/news_article_created.html', context))


@shared_task()
def send_email_forum(instance):
    """Send email when a new forum created."""
    queryset = User.objects.filter(is_active=True, is_superuser=False, email_notification_forum=True)
    all_emails = get_emails_from_queryset(queryset)
    context = {
        'domain':DOMAIN,
        'id': instance.pk
    }
    EMAILER.send_email(all_emails, 'Python @ ФМИ - Нов форум',
                       render_to_string('emails/forum_created.html', context))


@shared_task()
def send_email_homework(instance):
    """Send email when a new homework becomes visible."""
    queryset = User.objects.filter(is_active=True, is_superuser=False, email_notification_homework=True)
    all_emails = get_emails_from_queryset(queryset)
    context = {
        'domain':DOMAIN,
        'id': instance.pk
    }
    EMAILER.send_email(all_emails, 'Python @ ФМИ - Ново домашно',
                       render_to_string('emails/homework_created.html', context))


@shared_task()
def send_email_challenge(instance):
    """Send email when a new challenge becomes visible."""
    queryset = User.objects.filter(is_active=True, is_superuser=False, email_notification_challenge=True)
    all_emails = get_emails_from_queryset(queryset)
    context = {
        'domain':DOMAIN,
        'id': instance.pk
    }
    EMAILER.send_email(all_emails, 'Python @ ФМИ - Ново предизвикателство',
                       render_to_string('emails/challenge_created.html', context))


"""
Signals
"""


@receiver(post_save, sender=NewsArticle)
def newsarticle_action(sender, instance, created, **kwargs):
    if not created:
        # Modifying an existing article - nothing to do
        return False
    if os.environ.get('SHRUBBERY_ENV') == 'prd':
        send_email_newsarticle.delay(instance)
    else:
        send_email_newsarticle(instance)


@receiver(post_save, sender=Forum)
def forum_action(sender, instance, created, **kwargs):
    if not created:
        # Modifying an existing forum - nothing to do
        return False
    if os.environ.get('SHRUBBERY_ENV') == 'prd':
        send_email_forum.delay(instance)
    else:
        send_email_forum(instance)


@receiver(post_save, sender=Homework)
def homework_action(sender, instance, created, **kwargs):
    if not instance.hidden and not instance.email_sent:
        instance.email_sent = True
        instance.save()
        if os.environ.get('SHRUBBERY_ENV') == 'prd':
            send_email_homework.delay(instance)
        else:
            send_email_homework(instance)


@receiver(post_save, sender=Challenge)
def challenge_action(sender, instance, created, **kwargs):
    if not instance.hidden and not instance.email_sent:
        instance.email_sent = True
        instance.save()
        if os.environ.get('SHRUBBERY_ENV') == 'prd':
            send_email_challenge.delay(instance)
        else:
            send_email_challenge(instance)
