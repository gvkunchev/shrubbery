from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from users.models import Student, ProfilePicturePoints
from homeworks.models import Homework
from homeworksolutions.models import HomeworkSolution, HomeworkSolutionTeacherPoints
from challenges.models import Challenge
from challengesolutions.models import ChallengeSolution, ChallengeSolutionTeacherPoints
from points.models import PointsGiver


# Constant holding all models in the project
ALL_MODELS = apps.get_models()
# Constant holding all points givers in the project
POINTS_GIVER_MODELS = []
for model in ALL_MODELS:
    if issubclass(model, PointsGiver):
        POINTS_GIVER_MODELS.append(model)



def get_all_points():
    """Collect all points given."""
    points = []
    for model in POINTS_GIVER_MODELS:
        if model is HomeworkSolutionTeacherPoints:
            for object in model.objects.filter(solution__homework__verified=True):
                points.append(object.points)
        elif model is ChallengeSolutionTeacherPoints:
            for object in model.objects.filter(solution__challenge__verified=True):
                points.append(object.points)
        elif model is HomeworkSolution:
            for object in model.objects.filter(homework__verified=True):
                points.append(object.points)
        elif model is ChallengeSolution:
            for object in model.objects.filter(challenge__verified=True):
                points.append(object.points)
        else:
            for object in model.objects.all():
                points.append(object.points)
    return points


def get_all_points_per_user(user):
    """Collect all points for a particular user."""
    points = []
    for model in POINTS_GIVER_MODELS:
        if hasattr(model, 'author'):
            for object in model.objects.filter(author=user):
                points.append(object.points)
        elif hasattr(model, 'owner'):
            for object in model.objects.filter(owner=user):
                points.append(object.points)
        elif hasattr(model, 'solution'):
            if model is HomeworkSolutionTeacherPoints:
                for object in model.objects.filter(solution__author=user, solution__homework__verified=True):
                    points.append(object.points)
            elif model is ChallengeSolutionTeacherPoints:
                for object in model.objects.filter(solution__author=user, solution__challenge__verified=True):
                    points.append(object.points)
            else:
                raise Exception("Can't collect all points.")
    return points


def memoize_user(func):
    """Memoize the scores for all users to boost performance."""
    memoized = {}
    def wrapped(user):
        all_points = get_all_points_per_user(user)
        if all_points != memoized.get(user.full_name, {}).get('all_points'):
            memoized[user.full_name] = {
                'all_points': all_points,
                'result': func(user)
            }
        return memoized[user.full_name]['result']
    return wrapped


def memoize(func):
    """Memoize the scores for all users to boost performance."""
    memoized = None
    result = None
    def wrapped(*args, **kwargs):
        nonlocal memoized
        nonlocal result
        all_points = get_all_points()
        if all_points != memoized:
            memoized = all_points
            result = func(*args, **kwargs)
        return result
    return wrapped


@memoize_user
def get_point_summary(user):
    """Get points summary for a user."""
    points = {
        'profile_picture': 0,
        'comments': 0,
        'vouchers': 0
    }
    # Profile picture
    try:
        profile_picture_points =  ProfilePicturePoints.objects.get(owner=user)
        points['profile_picture'] = profile_picture_points.points
    except ObjectDoesNotExist:
        points['profile_picture'] = 0
    # Comments
    for comment in user.forumcomment_set.values():
        points['comments'] += comment.get('points', 0)
    for comment in user.homeworkcomment_set.values():
        points['comments'] += comment.get('points', 0)
    for comment in user.homeworksolutioncomment_set.values():
        points['comments'] += comment.get('points', 0)
    for comment in user.challengecomment_set.values():
        points['comments'] += comment.get('points', 0)
    for comment in user.challengesolutioncomment_set.values():
        points['comments'] += comment.get('points', 0)
    # Vouchers
    for voucher in user.voucher_set.values():
        points['vouchers'] += voucher.get('points', 0)
    # Homeworks
    for homework_solution in user.homeworksolution_set.values():
        if Homework.objects.get(pk=homework_solution.get('homework_id')).verified:
            teacher_points = HomeworkSolution.objects.get(pk=homework_solution.get('id')).homeworksolutionteacherpoints.points
            points[f"homework_{homework_solution.get('homework_id')}"] = homework_solution.get('points', 0) + teacher_points
    # Challenges
    for challenge_solution in user.challengesolution_set.values():
        if Challenge.objects.get(pk=challenge_solution.get('challenge_id')).verified:
            teacher_points = ChallengeSolution.objects.get(pk=challenge_solution.get('id')).challengesolutionteacherpoints.points
            points[f"challenge_{challenge_solution.get('challenge_id')}"] = challenge_solution.get('points', 0) + teacher_points
    # Exams
    for exam in user.examresult_set.values():
        points[f"exam_{exam.get('exam_id')}"] = exam.get('points', 0)
    # Total
    points['total'] = sum(points.values())
    return points


@memoize
def get_scoreboard_summary():
    """Get ranks for users."""
    data = []
    sudents_obj = Student.objects.filter(is_active=True)
    for student in sudents_obj:
        data_item = {'student': student}
        data_item.update(get_point_summary(student))
        data.append(data_item)
    data.sort(key=lambda x: x['total'], reverse=True)
    # Assign rankings
    all_scores = [x['total'] for x in data]
    all_unique_scores = sorted(list(set(all_scores)))
    for data_item in data:
        data_item['rank'] = len(all_unique_scores) - all_unique_scores.index(data_item['total'])
    return data


def get_rank_and_points(user):
    """Get rank and total points for a users."""
    summary = get_scoreboard_summary()
    for item in summary:
        if item['student'].pk == user.pk:
            return {
                'rank': item['rank'],
                'student_count': len(Student.objects.filter(is_active=True)),
                'total': item['total']
            }
