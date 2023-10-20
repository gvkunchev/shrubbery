from abc import ABC, abstractmethod
import os
import uuid
import json
import shutil
import subprocess
import tempfile

from django.conf import settings

from .models import Challenge
from challengesolutions.models import ChallengeSolution


class TestsRunner(ABC):
    """Tests runner for full and sanity test."""

    SANDBOX_MATRIX = '/var/shrubbery/sandbox/sandbox-origin'
    SANDBOX_TMP_COPY = '/var/shrubbery/sandbox/sandbox{}'
    TEST_RUNNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_runner.py')
    TIMEOUT = 2 # seconds
    TEST_KEY = None # To be set in child classes

    def __init__(self):
        """Initializator."""
        self._work_dir = None
        self._temp_id = uuid.uuid4()
        self._prd = os.environ.get('SHRUBBERY_ENV') == 'prd'
        self._prepare_data()
        self._prepare_env()
        self._execute()
        self._cleanup()

    @abstractmethod
    def _prepare_data(self):
        pass

    def _prepare_env(self):
        """Prepare the environment."""
        if self._prd:
            # Create sandbox filesystem
            self._work_dir = self.SANDBOX_TMP_COPY.format(self._temp_id)
            os.system(f'cp -r {self.SANDBOX_MATRIX} {self._work_dir}')
            # Copy the test runner
            shutil.copyfile(self.TEST_RUNNER, os.path.join(self._work_dir, 'tmp/test_runner.py'))
            # Copy the test itself
            with open(os.path.join(self._work_dir, 'tmp/test.py'), 'w') as f:
                f.write(getattr(self._challenge, self.TEST_KEY))
        else:
            # Create a temp directory
            self._work_dir = os.path.join(tempfile.gettempdir(), f'challenge{self._temp_id}')
            os.mkdir(self._work_dir)
            # Copy the test runner
            shutil.copyfile(self.TEST_RUNNER, os.path.join(self._work_dir, 'test_runner.py'))
            # Copy the test itself
            with open(os.path.join(self._work_dir, 'test.py'), 'w') as f:
                f.write(getattr(self._challenge, self.TEST_KEY))
    
    def _prepare_command(self, solution):
        """Prepare the solution in place and the command to run the test."""
        source_code = os.path.join(settings.MEDIA_ROOT, solution.content.path)
        if self._prd:
            # Copy the solution
            shutil.copy(source_code, os.path.join(self._work_dir, 'tmp/solution.py'))
            # Build the command
            return (f'runuser -l tester -c "env -i /usr/sbin/chroot {self._work_dir} '
                     '/usr/bin/python3.10 /tmp/test_runner.py /tmp/test.py"')
        else:
            # Copy the solution
            shutil.copy(source_code, os.path.join(self._work_dir, 'solution.py'))
            # Build the command
            test_runner = os.path.join(self._work_dir, 'test_runner.py')
            test = os.path.join(self._work_dir, 'test.py')
            return f'python {test_runner} {test}'
        
    @abstractmethod
    def _execute(self):
        pass

    def _cleanup(self):
        """Cleanup temp dirs and release the model."""
        shutil.rmtree(self._work_dir)


class FullTestsRunner(TestsRunner):
    """Runner for challenge full tests."""

    TEST_KEY = 'full_test'

    def __init__(self, challenge_pk):
        '''Initializator.'''
        self._challenge_pk = challenge_pk
        self._challenge = None
        self._solutions = None
        super(FullTestsRunner, self).__init__()
    
    def _prepare_data(self):
        """Prepare the data from database."""
        self._challenge = Challenge.objects.get(pk=self._challenge_pk)
        self._solutions = ChallengeSolution.objects.filter(challenge=self._challenge)
    
    def _execute(self):
        """Execute all tests."""
        for solution in self._solutions:
            command = self._prepare_command(solution)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, _ = process.communicate(timeout=self.TIMEOUT)
                json_result = json.loads(stdout)
                solution.passed_tests = len(json_result['passed'])
                solution.failed_tests = len(json_result['failed'])
                solution.result = json_result['log']
            except subprocess.TimeoutExpired:
                solution.passed_tests = 0
                solution.failed_tests = 0
                solution.result = 'Timed out.'
            finally:
                process = subprocess.Popen('killall -9 -u tester', shell=True)
            solution.save()
            solution.assign_points()

    def _cleanup(self):
        """Cleanup temp dirs and release the model."""
        super(FullTestsRunner, self)._cleanup()
        self._challenge.executing_tests = False
        self._challenge.save()


class SanityTestsRunner(TestsRunner):
    """Runner for challenge sanity tests."""

    TEST_KEY = 'sanity_test'

    def __init__(self, solution):
        '''Initializator.'''
        self._solution = solution
        self._json_result = None
        super(SanityTestsRunner, self).__init__()
    
    def _prepare_data(self):
        """Prepare the data from database."""
        self._challenge = self._solution.challenge
    
    def _execute(self):
        """Execute all tests."""
        command = self._prepare_command(self._solution)
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            stdout, _ = process.communicate(timeout=self.TIMEOUT)
            self._json_result = json.loads(stdout)
        except subprocess.TimeoutExpired:
            self._json_result = {
                'failed': 0,
                'passed': 0,
                'log': 'Timed out'
            }
        finally:
            process = subprocess.Popen('killall -9 -u tester', shell=True)

    def _cleanup(self):
        """Cleanup temp dirs and release the model."""
        super(SanityTestsRunner, self)._cleanup()
    
    def get_results(self):
        """Get test results."""
        return self._json_result
