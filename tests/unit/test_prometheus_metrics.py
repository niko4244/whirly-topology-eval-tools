import pytest
from prometheus_client import CollectorRegistry
from monitoring.prometheus_metrics import REQUEST_TIME, FAILED_REQUESTS, LOGIN_ATTEMPTS, ACTIVE_USERS

def test_counters_and_gauges():
    # Simulate increments
    FAILED_REQUESTS.inc()
    LOGIN_ATTEMPTS.inc(2)
    ACTIVE_USERS.set(10)

    # Check current values
    assert FAILED_REQUESTS._value.get() >= 1
    assert LOGIN_ATTEMPTS._value.get() >= 2
    assert ACTIVE_USERS._value.get() == 10

def test_summary_timer():
    with REQUEST_TIME.time():
        pass  # Simulate request