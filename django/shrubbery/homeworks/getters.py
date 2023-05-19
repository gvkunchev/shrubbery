from .models import Homework


def get_active_homeworks():
    """Get actie homework if any."""
    return Homework.objects.filter(hidden=False, verified=False)
