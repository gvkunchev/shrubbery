import os
import subprocess
import sys

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from shrubbery.view_decorators import is_teacher

from .models import Challenge, ChallengeComment
from .forms import ChallengeForm, ChallengeCommentForm

from comments.views import AddComment, EditComment, DeleteComment, SetCommentStar

from .tasks import run_challenge_tests


def challenges(request):
    '''Challenges page.'''
    return render(request, "challenges/challenges.html", {'challenges': Challenge.objects.all()})


@is_teacher
def add_challenge(request):
    '''Add new challenge.'''
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'author': request.user})
        form = ChallengeForm(data)
        if form.is_valid():
            form.save()
            context = {
                'challenges': Challenge.objects.all(),
                'info': 'Успешно добави предизвикателство'
            }
            return render(request, "challenges/challenges.html", context)
        else:
            return render(request, "challenges/add_challenge.html", {'errors': form.errors})
    else:
        return render(request, "challenges/add_challenge.html")


def challenge(request, challenge):
    '''Challenge page.'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
        if challenge.hidden and not (request.user.is_authenticated and request.user.is_teacher):
            raise ObjectDoesNotExist()
        main_comments = challenge.comments.filter(parent=None)
        paginator = Paginator(main_comments, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    except ObjectDoesNotExist:
        return redirect('missing')
    return render(request, "challenges/challenge.html", {'challenge': challenge, 'comments': page_obj})


@is_teacher
def delete_challenge(request, challenge):
    '''Delete challenge.'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
    except ObjectDoesNotExist:
        return redirect('missing')
    if len(challenge.challengesolution_set.values()):
        context = {
            'challenges': Challenge.objects.all(),
            'error': 'Не можеш да изтриеш предизвикателство с вече предадени решения. Използвай конзолата.'
        }
    else:
        challenge.delete()
        context = {
            'challenges': Challenge.objects.all(),
            'info': 'Успешно изтри предизвикателство'
        }
    return render(request, "challenges/challenges.html", context)


@is_teacher
def edit_challenge(request, challenge):
    '''Edit challenge.'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'challenge': challenge
    }
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'author': request.user})
        form = ChallengeForm(data, instance=challenge)
        if form.is_valid():
            form.save()
            context['info'] = 'Успешно редактира предизвикателство'
        else:
            context['errors'] = form.errors
    return render(request, "challenges/edit_challenge.html", context)


@login_required
def answer_challenge_comment(request, challenge, parent):
    '''Answer challenge comment in a thread.'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
        parent = ChallengeComment.objects.get(pk=parent)
    except ObjectDoesNotExist:
        return redirect('missing')
    if request.method == 'POST':
        data = {
            'challenge': challenge,
            'content': request.POST.get('content'),
            'parent': parent,
            'author': request.user
        }
        form = ChallengeCommentForm(data)
        if form.is_valid():
            comment = form.save()
            return redirect(f"/challenge/{challenge.pk}?page={request.POST.get('page')}#comment{comment.pk}")
        else:
            return render(request, "challenges/answer_challenge_comment.html", {'challenge': challenge,
                                                                               'parent': parent,
                                                                               'errors': form.errors})
    else:
        return render(request, "challenges/answer_challenge_comment.html", {'challenge': challenge, 'parent': parent})


class AddChallengeComment(AddComment):
    HOST = Challenge
    FORM = ChallengeCommentForm
    HOST_KEY = 'challenge'


class EditChallengeComment(EditComment):
    HOST = Challenge
    FORM = ChallengeCommentForm
    HOST_KEY = 'challenge'
    COMMENT_MODEL = ChallengeComment
    TEMPLATE = 'challenges/edit_challenge_comment.html'


class DeleteChallengeComment(DeleteComment):
    HOST_KEY = 'challenge'
    COMMENT_MODEL = ChallengeComment


class AddChallengeCommentStar(SetCommentStar):
    HOST_KEY = 'challenge'
    COMMENT_MODEL = ChallengeComment
    STATUS = True


class RemoveChallengeCommentStar(SetCommentStar):
    HOST_KEY = 'challenge'
    COMMENT_MODEL = ChallengeComment
    STATUS = False


@is_teacher
def run_tests(request, challenge):
    '''Run challenge tests.'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
        if challenge.executing_tests:
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        return redirect('missing')
    challenge.executing_tests = True
    challenge.save()
    if os.environ.get('SHRUBBERY_ENV') == 'prd':
        run_challenge_tests.delay(challenge.pk)
    else:
        run_challenge_tests(challenge.pk)
    return redirect(request.GET.get('goto', f'/challenge/{challenge.pk}'))


@is_teacher
def get_slackers(request, challenge):
    '''Compare solutions and get slackers report..'''
    try:
        challenge = Challenge.objects.get(pk=challenge)
    except ObjectDoesNotExist:
        return redirect('missing')
    path = os.path.join(settings.MEDIA_ROOT, 'challengesolutions', str(challenge.pk))
    slackers_run = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'slackers.py'), path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = slackers_run.communicate()
    return HttpResponse(stdout)
