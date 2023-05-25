import os
import shutil
import subprocess
import tempfile

from django.conf import settings
from celery import shared_task


from .models import Homework
from homeworksolutions.models import HomeworkSolution


class TestsRunner:
    """Runner for homework tests."""

    SANDBOX_MATRIX = '/var/shrubbery/sandbox/sandbox-origin'
    SANDBOX_TMP_COPY = '/var/shrubbery/sandbox/sandbox{}'

    def __init__(self, homework_pk):
        '''Initializator.'''
        self._homework_pk = homework_pk
        self._homework = None
        self._solutions = None
        self._work_dir = None
        self._prepare_data()
        self._prepare_env()
        self._execute()
        self._cleanup()
    
    def _prepare_data(self):
        """Prepare the data from database."""
        self._homework = Homework.objects.get(pk=self._homework_pk)
        self._solutions = HomeworkSolution.objects.filter(homework=self._homework)
    
    def _prepare_env(self):
        """Prepare the environment."""
        if os.environ.get('SHRUBBERY_ENV') == 'prd':
            self._work_dir = self.SANDBOX_TMP_COPY.format(self._homework_pk)
            os.system(f'cp -r {self.SANDBOX_MATRIX} {self._work_dir}')
            with open(os.path.join(self._work_dir, 'tmp/test.py'), 'w') as f:
                f.write(self._homework.full_test)
        else:
            self._work_dir = os.path.join(tempfile.gettempdir(), f'homework{self._homework_pk}')
            os.mkdir(self._work_dir)
            with open(os.path.join(self._work_dir, 'test.py'), 'w') as f:
                f.write(self._homework.full_test)
    
    def _execute(self):
        """Execute all tests."""
        for solution in self._solutions:
            source_code = os.path.join(settings.MEDIA_ROOT, solution.content.path)
            if os.environ.get('SHRUBBERY_ENV') == 'prd':
                shutil.copy(source_code, os.path.join(self._work_dir, 'tmp/solution.py'))
                process = subprocess.Popen('env -i '
                                        f'/usr/sbin/chroot {self._work_dir} '
                                        '/usr/bin/python3.10 /tmp/test.py', shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
            else:
                shutil.copy(source_code, os.path.join(self._work_dir, 'solution.py'))
                test_location = os.path.join(self._work_dir, 'test.py')
                process = subprocess.Popen(f'python {test_location}', shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=2) # seconds
            solution.results = f"{stdout.decode('utf-8')}\n\n{stderr.decode('utf-8')}"
            # TODO: Assign points
            solution.save()

    def _cleanup(self):
        """Cleanup temp dirs and release the model."""
        shutil.rmtree(self._work_dir)
        self._homework.executing_tests = False
        self._homework.save()


@shared_task()
def run_homework_tests(homework_pk):
    """Tun tests for all solutions of a homework.."""
    TestsRunner(homework_pk)
