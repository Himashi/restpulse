import time
import uuid
import logging
from typing import Callable, Any

logger = logging.getLogger("restpulse.telemetry")

class TelemetryMiddleware:
    """
    Middleware that injects request correlation IDs and logs structured
    telemetry data (latency, status code, method, URL).
    """
    def __init__(self, logger_instance: logging.Logger = None):
        self.logger = logger_instance or logger

    def __call__(self, request: Any, next_call: Callable[[Any], Any]) -> Any:
        request_id = str(uuid.uuid4())
        if hasattr(request, "headers"):
            request.headers.setdefault("X-Request-ID", request_id)

        start_time = time.perf_counter()
        
        self.logger.info(
            f"Started request [{request_id}] {getattr(request, 'method', 'GET')} {getattr(request, 'url', '')}"
        )

        try:
            response = next_call(request)
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            self.logger.info(
                f"Completed request [{request_id}] "
                f"Status: {getattr(response, 'status_code', 200)} | Duration: {duration_ms:.2f}ms"
            )
            
            if hasattr(response, "metrics"):
                response.metrics = {"request_id": request_id, "duration_ms": duration_ms}
                
            return response

        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.logger.error(
                f"Failed request [{request_id}] after {duration_ms:.2f}ms: {str(exc)}"
            )
            raise