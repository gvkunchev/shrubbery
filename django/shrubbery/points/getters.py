from django.core.exceptions import ObjectDoesNotExist

from users.models import ProfilePicturePoints


def get_point_summary(user):
    """Get points summary for a user."""
    points = {
        'profile_picture': 0,
        'comments': 0
    }
    # Profile picture
    try:
        profile_picture_points =  ProfilePicturePoints.objects.get(owner=user)
        points['profile_picture'] = profile_picture_points.points
    except ObjectDoesNotExist:
        points['profile_picture'] = 0
    # Comments
    for comment in user.forumcomment_set.values():
        print(comment)
        points['comments'] += comment.get('points', 0)
    points['total'] = sum(points.values())
    return points
