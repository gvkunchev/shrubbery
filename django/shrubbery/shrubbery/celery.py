import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shrubbery.settings')


app = Celery('shrubbery')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'alert_for_new_solution_comments': {
        'task': 'alert_for_new_solution_comments',
        'schedule': crontab(minute=0), # Hourly UTC
    },
    # TODO: Put back to enable points backup
    #'backup_points': {
    #    'task': 'backup_points',
    #    'schedule': crontab(minute=0, hour=0) # Daily at midnight UTC
    #}
}