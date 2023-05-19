from django.core.exceptions import ObjectDoesNotExist

from users.models import Student, ProfilePicturePoints


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
    # Vouchers
    for voucher in user.voucher_set.values():
        points['vouchers'] += voucher.get('points', 0)
    # Exams
    for exam in user.examresult_set.values():
        points[f"exam_{exam.get('exam_id')}"] = exam.get('points', 0)
    # Total
    points['total'] = sum(points.values())
    return points


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
