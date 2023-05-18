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

@register.filter()
def activate_link(request_path, url):
    """Determine whether to active a link in the navbar ot not."""
    if url == '/':
        return request_path == '/'
    return url.rstrip('s') in request_path