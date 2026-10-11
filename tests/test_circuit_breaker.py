import pytest
from restpulse.middleware.circuit_breaker import CircuitBreakerMiddleware, CircuitOpenError

class MockRequest:
    pass

def test_circuit_breaker_trips_and_recovers():
    cb = CircuitBreakerMiddleware(failure_threshold=2, recovery_timeout=1.0)
    
    def failing_handler(req):
        raise RuntimeError("Service Down")

    # 1. Trigger failures up to threshold
    with pytest.raises(RuntimeError):
        cb(MockRequest(), failing_handler)
    
    assert cb.state == "CLOSED"

    # Second failure should trip the breaker to OPEN
    with pytest.raises(RuntimeError):
        cb(MockRequest(), failing_handler)
    
    assert cb.state == "OPEN"

    # 2. Subsequent requests should fail fast with CircuitOpenError
    with pytest.raises(CircuitOpenError):
        cb(MockRequest(), lambda r: "success")