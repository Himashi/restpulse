import time
import logging
from typing import Callable, Any

logger = logging.getLogger("restpulse.circuit_breaker")

class CircuitOpenError(Exception):
    """Raised when a request is blocked because the circuit breaker is OPEN."""
    pass

class CircuitBreakerMiddleware:
    """
    Middleware implementing the Circuit Breaker pattern with three states:
    CLOSED (normal), OPEN (failing fast), and HALF-OPEN (testing recovery).
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 10.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    def __call__(self, request: Any, next_call: Callable[[Any], Any]) -> Any:
        current_time = time.time()

        # Check if an OPEN circuit should transition to HALF-OPEN for testing
        if self.state == "OPEN":
            if current_time - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                logger.info("Circuit breaker state changed: OPEN -> HALF-OPEN")
            else:
                raise CircuitOpenError("Circuit breaker is OPEN. Request blocked.")

        try:
            response = next_call(request)
            
            # Successful request resets the circuit
            if self.state in ("HALF-OPEN", "OPEN"):
                logger.info(f"Circuit breaker recovered. State changed: {self.state} -> CLOSED")
            self.state = "CLOSED"
            self.failures = 0
            return response

        except Exception as exc:
            self.failures += 1
            self.last_failure_time = current_time
            logger.error(f"Request failed. Failure count: {self.failures}/{self.failure_threshold}")

            if self.failures >= self.failure_threshold or self.state == "HALF-OPEN":
                self.state = "OPEN"
                logger.warning("Circuit breaker tripped to OPEN state.")
            raise exc