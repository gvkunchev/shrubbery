from django.shortcuts import render
from shrubbery.view_decorators import is_student

from .models import KingArthur


@is_student
def achievements(request):
    """Achievements list page."""
    context = {
        'achievements': [
            {
                'name': 'king_arthur',
                'model': KingArthur,
                'achieved': KingArthur.objects.get(owner=request.user).achieved
            }
        ]
    }
    return render(request, "achievements/achievements_list.html", context)
