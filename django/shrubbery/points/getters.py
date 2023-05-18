from django.core.exceptions import ObjectDoesNotExist

from users.models import ProfilePicturePoints


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
    # Vouchers
    for voucher in user.voucher_set.values():
        points['vouchers'] += voucher.get('points', 0)
    # Total
    points['total'] = sum(points.values())
    return points
