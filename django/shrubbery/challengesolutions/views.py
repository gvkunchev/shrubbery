from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from shrubbery.view_decorators import is_teacher

from challenges.models import Challenge
from users.models import Teacher
from .models import (ChallengeSolution, ChallengeSolutionComment,
                     ChallengeSolutionHistory, ChallengeSolutionInlineComment,
                     ChallengeSolutionTeacherPoints)
from .forms import (ChallengeSolutionForm, ChallengeSolutionCommentForm,
                    ChallengeSolutionInlineCommentForm,
                    ChallengeSolutionTeacherPointsForm)

from comments.views import AddComment, EditComment, DeleteComment, SetCommentStar

from challenges.tasks import run_sanity_test


def challenge_solutions(request, challenge):
    """Challenge solutions page."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        if challenge.hidden or not challenge.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.user.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'challenge': challenge,
        'solutions': challenge.challengesolution_set.all()
    }
    return render(request, "challenge_solutions/solutions.html", context)


def challenge_solution(request, challenge, solution):
    """Challenge solution page."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        solution = ChallengeSolution.objects.get(pk=solution)
        if challenge.hidden or not challenge.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if request.user.is_student and request.user.pk != solution.author.pk:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'challenge': challenge,
        'solution': solution,
        'content': solution.get_content(),
        'comments': solution.comments,
        'commit_message': solution.commit_message,
        'history': ChallengeSolutionHistory.objects.filter(solution=solution),
        'inline_comments': ChallengeSolutionInlineComment.objects.filter(solution=solution),
    }
    return render(request, "challenge_solutions/solution.html", context)

@is_teacher
def set_teacher_points(request, challenge, solution):
    """Set teacher points to a solution."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        solution = ChallengeSolution.objects.get(pk=solution)
        teacher_points = ChallengeSolutionTeacherPoints.objects.get(solution=solution)
    except ObjectDoesNotExist:
        return redirect('missing')
    data = {
        'solution': solution,
        'points': request.POST.get('teacher_points', 0)
    }
    form = ChallengeSolutionTeacherPointsForm(data, instance=teacher_points)
    if form.is_valid():
        form.save()
    return redirect(f"/challenge/{challenge.pk}/solution/{solution.pk}")

@is_teacher
def edit_internal_notes(request, challenge, solution):
    """Edit internal notes for a challenge solution."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        solution = ChallengeSolution.objects.get(pk=solution)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.internal_notes = request.POST.get('internal_notes', '')
    solution.save()
    return redirect(f"/challenge/{challenge.pk}/solution/{solution.pk}")

def add_challenge_solution(request, challenge):
    """Add challenge solution page."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        if not challenge.can_upload:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.user.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'challenge': challenge
    }
    if request.method == 'POST':
        data = {
            'author': request.user,
            'challenge': challenge,
            'commit_message': request.POST.get('commit_message', '')[:50] # Ensure no more than 50 chars
        }
        history_object = None
        try:
            # If there is already an uploaded solution,
            # move it to history and replace with the new one
            existing_solution = ChallengeSolution.objects.get(author=request.user, challenge=challenge)
            history_object = existing_solution.send_to_history()
            form = ChallengeSolutionForm(data, request.FILES, instance=existing_solution)
        except ObjectDoesNotExist:
            form = ChallengeSolutionForm(data, request.FILES)
        if form.is_valid():
            solution = form.save()
            solution.assign_line_count()
            if history_object is not None:
                history_object.assign_diff_to(solution)
            try:
                results = run_sanity_test(solution)
                if len(results['failed']) or not len(results['passed']):
                    raise ValidationError(results['log'])
            except ValidationError as error:
                context['verification_error'] = error.message
                return render(request, "challenge_solutions/add_solution.html", context)
            return redirect(f'/challenge/{challenge.pk}/solution/{solution.pk}')
        else:
            context['errors'] = form.errors
    return render(request, "challenge_solutions/add_solution.html", context)


@is_teacher
def subscribe(request, challenge, solution):
    """Subscribe to a challenge."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        solution = ChallengeSolution.objects.get(pk=solution)
        teacher = Teacher.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.subscribers.add(teacher)
    return redirect(f"/challenge/{challenge.pk}/solution/{solution.pk}")


@is_teacher
def unsubscribe(request, challenge, solution):
    """Unsubscribe to a challenge."""
    try:
        challenge = Challenge.objects.get(pk=challenge)
        solution = ChallengeSolution.objects.get(pk=solution)
        teacher = Teacher.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.subscribers.remove(teacher)
    return redirect(f"/challenge/{challenge.pk}/solution/{solution.pk}")



class AddChallengeSolutionComment(AddComment):
    HOST = ChallengeSolution
    FORM = ChallengeSolutionCommentForm
    HOST_KEY = 'solution'


class EditChallengeSolutionComment(EditComment):
    HOST = ChallengeSolution
    FORM = ChallengeSolutionCommentForm
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionComment
    TEMPLATE = 'challenge_solutions/edit_challenge_solution_comment.html'


class DeleteChallengeSolutionComment(DeleteComment):
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionComment


class AddChallengeSolutionCommentStar(SetCommentStar):
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionComment
    STATUS = True


class RemoveChallengeSolutionCommentStar(SetCommentStar):
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionComment
    STATUS = False


class EditChallengeSolutionInlineComment(EditComment):
    HOST = ChallengeSolution
    FORM = ChallengeSolutionInlineCommentForm
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionInlineComment
    TEMPLATE = 'challenge_solutions/edit_challenge_solution_inline_comment.html'


class DeleteChallengeSolutionInlineComment(DeleteComment):
    HOST_KEY = 'solution'
    COMMENT_MODEL = ChallengeSolutionInlineComment


class AddChallengeSolutionInlineComment(AddComment):
    HOST = ChallengeSolution
    FORM = ChallengeSolutionInlineCommentForm
    HOST_KEY = 'solution'