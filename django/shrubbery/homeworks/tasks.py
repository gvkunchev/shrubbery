import os
import shutil
import subprocess

from django.conf import settings
from celery import shared_task


from .models import Homework
from homeworksolutions.models import HomeworkSolution


@shared_task()
def run_homework_tests(homework_pk):
    """Tun tests for all solutions of a homework.."""
    SANDBOX_MATRIX = '/var/shrubbary/sandbox/sandbox-origin'
    SANDBOX_TMP_COPY = f'/var/shrubbary/sandbox/sandbox{homework_pk}'
    homework = Homework.objects.get(pk=homework_pk)
    solutions = HomeworkSolution.objects.filter(homework=homework)

    os.system(f'cp -r {SANDBOX_MATRIX} {SANDBOX_TMP_COPY}')
    with open(os.path.join(SANDBOX_TMP_COPY, 'tmp/test.py'), 'w') as f:
        f.write(homework.full_test)
    for solution in solutions:
        source_code = os.path.join(settings.MEDIA_ROOT, solution.content.path)
        shutil.copy(source_code, os.path.join(SANDBOX_TMP_COPY, 'tmp/solution.py'))
        process = subprocess.Popen('env -i '
                                   f'/usr/sbin/chroot {SANDBOX_TMP_COPY} '
                                   '/usr/bin/python3.10 /tmp/test.py', shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        result = process.communicate(timeout=2) # seconds
        solution.results = result
        # TODO: Assign points
        solution.save()
    shutil.rmtree(SANDBOX_TMP_COPY) 

    homework.executing_tests = False
    homework.save()
