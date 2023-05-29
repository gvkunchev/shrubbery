from .models import Challenge


def get_active_challenges():
    """Get actie challenge if any."""
    return Challenge.objects.filter(hidden=False, verified=False)
