import time

from celery import shared_task


from .models import Homework


@shared_task()
def run_homework_tests(homework_pk):
    """Tun tests for all solutions of a homework.."""
    homework = Homework.objects.get(pk=homework_pk)
    time.sleep(5)
    with open('/tmp/tests', 'w') as f:
        f.write('Done')
    homework.executing_tests = False
    homework.save()
