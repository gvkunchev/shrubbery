# Run a unittest file on a solution
# and get the result in a JSON.
# Thanks to https://github.com/skanev/evans
import importlib
import io
import json
import os
import sys
import unittest
import traceback

TEST_PROCESS_TIMEOUT = 2  # in seconds.


class StdBuffer:
    def __init__(self, buffer):
        self.buffer = buffer

    def __enter__(self):
        self.stds = sys.stdin, sys.stderr, sys.stdout
        sys.stdin = self.buffer
        sys.stderr = self.buffer
        sys.stdout = self.buffer

    def __exit__(self, *args, **kwargs):
        sys.stdin, sys.stderr, sys.stdout = self.stds


class EmptyTestResult:
    all_tests = []
    failures = []
    errors = []
    log = ''


class DiligentTestSuite(unittest.TestSuite):
    def __init__(self, tests=()):
        super().__init__()
        tests = [test for test in tests]
        for index, test in enumerate(tests):
            try:
                test_method = getattr(test, test._testMethodName)
                setattr(tests[index],
                        test._testMethodName,
                        test_method)
            except AttributeError:
                pass

        self.addTests(tests)

    def _removeTestAtIndex(self, index):
        """Just to avoid our suite doing that..."""


class DiligentTestLoader(unittest.loader.TestLoader):
    suiteClass = DiligentTestSuite


class DiligentTextTestRunner(unittest.TextTestRunner):
    all_tests = []

    def run(self, test):
        result = super().run(test)
        for test_suite in test._tests:
            for test in test_suite._tests:
                self.all_tests.append(str(test))
        result.all_tests = self.all_tests
        return result


def main(test_module):
    buffer = io.StringIO()
    sys.path = [os.path.dirname(test_module)] + sys.path

    with StdBuffer(buffer):
        try:
            loaded_test = importlib.import_module('test', test_module)
            result = unittest.main(
                module=loaded_test,
                buffer=buffer,
                exit=False,
                testRunner=DiligentTextTestRunner,
                testLoader=DiligentTestLoader(),
            ).result
        except Exception as e:
            result = EmptyTestResult()
            print(e)
            traceback.print_tb(e.__traceback__)

    failed = [str(test[0]) for test in result.failures + result.errors]
    passed = [test for test in result.all_tests if test not in failed]

    return {
        'passed': passed,
        'failed': failed,
        'log': buffer.getvalue(),
    }


if __name__ == '__main__':
    try:
        initial_niceness = os.nice(0)
        os.nice(10 - initial_niceness)
    except:
        pass # Not a unix system - no niceness
    print(json.dumps(main(sys.argv.pop())))
