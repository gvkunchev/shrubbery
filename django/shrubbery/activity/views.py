from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from shrubbery.view_decorators import is_teacher

from .models import Action


@is_teacher
def activity(request):
    '''Activity page.'''
    all_actions = Action.objects.all()
    paginator = Paginator(all_actions, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "actions/actions.html", {'actions': page_obj})


@is_teacher
def force_seen(request, activity):
    '''Force seen on an activity.'''
    try:
        action = Action.objects.get(pk=activity)
        action.forced_seen = True
        action.save()
    except ObjectDoesNotExist:
        return redirect('missing')
    return redirect('activity:activity')
