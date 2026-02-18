from django.conf import settings

def export_settings(request):
    return {
        'YEAR': settings.YEAR
    }
