from celery import shared_task

from .test_runners import FullTestsRunner, SanityTestsRunner


@shared_task()
def run_challenge_tests(challenge_pk):
    """Run tests for all solutions of a challenge."""
    FullTestsRunner(challenge_pk)


@shared_task()
def run_sanity_test(solution):
    """Run sanity test for a single solution of a challenge."""
    return SanityTestsRunner(solution).get_results()
