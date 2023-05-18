from django import template

register = template.Library()


@register.simple_tag()
def create_list(*args):
    return args

@register.simple_tag(name='zip')
def zip_many(*args):
    return list(zip(*args))

@register.simple_tag()
def get_exam_results(data, exam):
    key = f'exam_{exam.pk}'
    return data.get(key, '-')
