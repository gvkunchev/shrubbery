from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from homeworks.models import Homework
from .models import (HomeworkSolution, HomeworkSolutionComment,
                     HomeworkSolutionHistory, HomeworkSolutionInlineComment)
from .forms import HomeworkSolutionForm, HomeworkSolutionCommentForm

from comments.views import AddComment, EditComment, DeleteComment, SetCommentStar

from homeworks.tasks import run_sanity_test


def homework_solutions(request, homework):
    """Homework solutions page."""
    try:
        homework = Homework.objects.get(pk=homework)
        if homework.hidden or not homework.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.user.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework,
        'solutions': HomeworkSolution.objects.filter(homework=homework)
    }
    return render(request, "homework_solutions/solutions.html", context)


def homework_solution(request, homework, solution):
    """Homework solution page."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
        if homework.hidden or not homework.verified:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if request.user.is_student and request.user.pk != solution.author.pk:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework,
        'solution': solution,
        'content': solution.get_content(),
        'comments': solution.comments,
        'history': HomeworkSolutionHistory.objects.filter(solution=solution),
        'inline_comments': HomeworkSolutionInlineComment.objects.filter(solution=solution),
    }
    return render(request, "homework_solutions/solution.html", context)


def add_homework_solution(request, homework):
    """Add homework solution page."""
    try:
        homework = Homework.objects.get(pk=homework)
        if not homework.can_upload:
            if not request.user.is_authenticated:
                raise ObjectDoesNotExist
            if not request.user.is_teacher:
                raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return redirect('missing')
    context = {
        'homework': homework
    }
    if request.method == 'POST':
        data = {
            'author': request.user,
            'homework': homework,
        }
        history_object = None
        try:
            # If there is already an uploaded solution,
            # move it to history and replace with the new one
            existing_solution = HomeworkSolution.objects.get(author=request.user, homework=homework)
            history_object = existing_solution.send_to_history()
            form = HomeworkSolutionForm(data, request.FILES, instance=existing_solution)
        except ObjectDoesNotExist:
            form = HomeworkSolutionForm(data, request.FILES)
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
                return render(request, "homework_solutions/add_solution.html", context)
            return redirect(f'/homework/{homework.pk}/solution/{solution.pk}')
        else:
            context['errors'] = form.errors
    return render(request, "homework_solutions/add_solution.html", context)


class AddHomeworkSolutionComment(AddComment):
    HOST = HomeworkSolution
    FORM = HomeworkSolutionCommentForm
    HOST_KEY = 'solution'


class EditHomeworkSolutionComment(EditComment):
    HOST = HomeworkSolution
    FORM = HomeworkSolutionCommentForm
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionComment
    TEMPLATE = 'homework_solutions/edit_homework_solution_comment.html'


class DeleteHomeworkSolutionComment(DeleteComment):
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionComment


class AddHomeworkSolutionCommentStar(SetCommentStar):
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionComment
    STATUS = True


class RemoveHomeworkSolutionCommentStar(SetCommentStar):
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionComment
    STATUS = False
