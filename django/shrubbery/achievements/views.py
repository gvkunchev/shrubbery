from django.shortcuts import render
from shrubbery.view_decorators import is_student

from .models import ACHIEVEMENTS


@is_student
def achievements(request):
    """Achievements list page."""
    context = {'achievements': []}
    for achievement in ACHIEVEMENTS:
        context['achievements'].append({
            'model': achievement,
            'achieved': achievement.objects.get(owner=request.user).achieved
        })
    return render(request, "achievements/achievements_list.html", context)
