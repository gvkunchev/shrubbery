from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from shrubbery.email import Emailer
from .tokens import account_activation_token

EMAILER = Emailer()


def send_activation_email(request, user):
    """Send email with activation link to a user."""
    current_site = get_current_site(request)
    mail_subject = 'Активирай своя акаунт за "Python @ ФМИ"'
    message = render_to_string('emails/activation_email.html', {
                    'user': user.full_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
    EMAILER.send_email([user.email], mail_subject, message)


def send_new_password_email(request, user):
    """Send email with link for changing the password to a user."""
    current_site = get_current_site(request)
    mail_subject = 'Смени пароалта на своя акаунт за "Python @ ФМИ"'
    message = render_to_string('emails/new_password_email.html', {
                    'user': user.full_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
    EMAILER.send_email([user.email], mail_subject, message)
