from django.shortcuts import render

from users.models import Student
from shrubbery.view_decorators import is_teacher

from .getters import get_point_summary


@is_teacher
def points(request):
    '''Points page.'''
    data = []
    sudents_obj = Student.objects.filter(is_active=True)
    for student in sudents_obj:
        data_item = {'student': student}
        data_item.update(get_point_summary(student))
        data.append(data_item)
    data.sort(key=lambda x: x['total'], reverse=True)
    return render(request, "points/points.html", {'data': data})


def scoreboard(request):
    '''Points page.'''
    data = []
    sudents_obj = Student.objects.filter(is_active=True)
    for student in sudents_obj:
        data_item = {'student': student}
        total = get_point_summary(student)['total']
        data_item.update({'total': total})
        data.append(data_item)
    data.sort(key=lambda x: x['total'], reverse=True)
    # Assign rankings
    all_scores = [x['total'] for x in data]
    all_unique_scores = sorted(list(set(all_scores)))
    for data_item in data:
        data_item['rank'] = len(all_unique_scores) - all_unique_scores.index(data_item['total'])
    return render(request, "scoreboard.html", {'data': data})
