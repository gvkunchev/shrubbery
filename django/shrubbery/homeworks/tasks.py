from celery import shared_task

from .test_runners import FullTestsRunner, SanityTestsRunner


@shared_task()
def run_homework_tests(homework_pk):
    """Run tests for all solutions of a homework.."""
    FullTestsRunner(homework_pk)


@shared_task()
def run_sanity_test(solution):
    """Run sanity test for a single solution of a homework.."""
    return SanityTestsRunner(solution).get_results()
