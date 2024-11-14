from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from shrubbery.view_decorators import is_teacher

from homeworks.models import Homework
from users.models import Teacher
from .models import (HomeworkSolution, HomeworkSolutionComment,
                     HomeworkSolutionHistory, HomeworkSolutionInlineComment,
                     HomeworkSolutionTeacherPoints)
from .forms import (HomeworkSolutionForm, HomeworkSolutionCommentForm,
                    HomeworkSolutionInlineCommentForm,
                    HomeworkSolutionTeacherPointsForm)

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
    solutions = list(HomeworkSolution.objects.filter(homework=homework))
    filtered_solutions = solutions[:]
    if request.user.is_authenticated and request.user.is_teacher:
        for solution in solutions:
            subscribers = map(lambda x: x.pk, solution.subscribers.all())
            if 'filter_subscribed' in request.GET:
                if request.user.pk in subscribers:
                    filtered_solutions.remove(solution)
            if 'filter_no_subscribers' in request.GET:
                if not len(solution.subscribers.all()):
                    filtered_solutions.remove(solution)
            if 'filter_foreign_subscribers_only' in request.GET:
                if solution in filtered_solutions and request.user.pk not in subscribers and len(solution.subscribers.all()):
                    filtered_solutions.remove(solution)
    context = {
        'homework': homework,
        'solutions': filtered_solutions
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
        'commit_message': solution.commit_message,
        'history': HomeworkSolutionHistory.objects.filter(solution=solution),
        'inline_comments': HomeworkSolutionInlineComment.objects.filter(solution=solution),
    }
    return render(request, "homework_solutions/solution.html", context)

@is_teacher
def set_teacher_points(request, homework, solution):
    """Set teacher points to a solution."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
        teacher_points = HomeworkSolutionTeacherPoints.objects.get(solution=solution)
    except ObjectDoesNotExist:
        return redirect('missing')
    data = {
        'solution': solution,
        'points': request.POST.get('teacher_points', 0)
    }
    form = HomeworkSolutionTeacherPointsForm(data, instance=teacher_points)
    if form.is_valid():
        form.save()
    return redirect(f"/homework/{homework.pk}/solution/{solution.pk}")

@is_teacher
def edit_internal_notes(request, homework, solution):
    """Edit internal notes for a homework solution."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.internal_notes = request.POST.get('internal_notes', '')
    solution.save()
    return redirect(f"/homework/{homework.pk}/solution/{solution.pk}")

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
            'commit_message': request.POST.get('commit_message', '')[:50] # Ensure no more than 50 chars
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


@is_teacher
def subscribe(request, homework, solution):
    """Subscribe to a homework."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
        teacher = Teacher.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.subscribers.add(teacher)
    return redirect(f"/homework/{homework.pk}/solution/{solution.pk}")


@is_teacher
def unsubscribe(request, homework, solution):
    """Unsubscribe to a homework."""
    try:
        homework = Homework.objects.get(pk=homework)
        solution = HomeworkSolution.objects.get(pk=solution)
        teacher = Teacher.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return redirect('missing')
    solution.subscribers.remove(teacher)
    return redirect(f"/homework/{homework.pk}/solution/{solution.pk}")


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


class EditHomeworkSolutionInlineComment(EditComment):
    HOST = HomeworkSolution
    FORM = HomeworkSolutionInlineCommentForm
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionInlineComment
    TEMPLATE = 'homework_solutions/edit_homework_solution_inline_comment.html'


class DeleteHomeworkSolutionInlineComment(DeleteComment):
    HOST_KEY = 'solution'
    COMMENT_MODEL = HomeworkSolutionInlineComment


class AddHomeworkSolutionInlineComment(AddComment):
    HOST = HomeworkSolution
    FORM = HomeworkSolutionInlineCommentForm
    HOST_KEY = 'solution'