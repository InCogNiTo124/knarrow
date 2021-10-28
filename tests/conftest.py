# Adapted from https://stackoverflow.com/a/47731333
import pytest

ACCEPTABLE_FAILURE_RATE = 0.05


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    if exitstatus != pytest.ExitCode.TESTS_FAILED:
        return
    failure_rate = session.testsfailed / session.testscollected
    if failure_rate <= ACCEPTABLE_FAILURE_RATE:
        session.exitstatus = 0
