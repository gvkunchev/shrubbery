import os
import json
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
    TEST_RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_runner.py')
    TIMEOUT = 2 # seconds

    def __init__(self, homework_pk):
        '''Initializator.'''
        self._homework_pk = homework_pk
        self._homework = None
        self._solutions = None
        self._work_dir = None
        self._prd = os.environ.get('SHRUBBERY_ENV') == 'prd'
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
        if self._prd:
            # Create sandbox filesystem
            self._work_dir = self.SANDBOX_TMP_COPY.format(self._homework_pk)
            os.system(f'cp -r {self.SANDBOX_MATRIX} {self._work_dir}')
            # Copy the test runner
            shutil.copyfile(self.TEST_RUNNER, os.path.join(self._work_dir, 'tmp/test_runner.py'))
            # Copy the test itself
            with open(os.path.join(self._work_dir, 'tmp/test.py'), 'w') as f:
                f.write(self._homework.full_test)
        else:
            # Create a temp directory
            self._work_dir = os.path.join(tempfile.gettempdir(), f'homework{self._homework_pk}')
            os.mkdir(self._work_dir)
            # Copy the test runner
            shutil.copyfile(self.TEST_RUNNER, os.path.join(self._work_dir, 'test_runner.py'))
            # Copy the test itself
            with open(os.path.join(self._work_dir, 'test.py'), 'w') as f:
                f.write(self._homework.full_test)
    
    def _execute(self):
        """Execute all tests."""
        for solution in self._solutions:
            source_code = os.path.join(settings.MEDIA_ROOT, solution.content.path)
            if self._prd:
                # Copy the solution
                shutil.copy(source_code, os.path.join(self._work_dir, 'tmp/solution.py'))
                # Build the command
                command = (f'env -i /usr/sbin/chroot {self._work_dir} '
                            '/usr/bin/python3.10 /tmp/test_runner.py /tmp/test.py')
            else:
                # Copy the solution
                shutil.copy(source_code, os.path.join(self._work_dir, 'solution.py'))
                # Build the command
                test_runner = os.path.join(self._work_dir, 'test_runner.py')
                test = os.path.join(self._work_dir, 'test.py')
                command = (f'python {test_runner} {test}')
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = process.communicate(timeout=self.TIMEOUT)
            json_result = json.loads(stdout)
            solution.passed_tests = len(json_result['passed'])
            solution.failed_tests = len(json_result['failed'])
            solution.result = json_result['log']
            solution.save()
            solution.assign_points()

    def _cleanup(self):
        """Cleanup temp dirs and release the model."""
        shutil.rmtree(self._work_dir)
        self._homework.executing_tests = False
        self._homework.save()


@shared_task()
def run_homework_tests(homework_pk):
    """Tun tests for all solutions of a homework.."""
    TestsRunner(homework_pk)
