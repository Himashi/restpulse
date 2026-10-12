import time
from typing import Callable, Any
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.propagate import inject

tracer = trace.get_tracer("restpulse.opentelemetry")

class OpenTelemetryMiddleware:
    """
    Middleware that instruments outbound HTTP requests with OpenTelemetry spans
    and injects W3C Trace Context headers for distributed tracing.
    """
    def __init__(self, tracer_instance=None):
        self.tracer = tracer_instance or tracer

    def __call__(self, request: Any, next_call: Callable[[Any], Any]) -> Any:
        method = getattr(request, "method", "GET").upper()
        url = getattr(request, "url", "unknown")
        
        span_name = f"HTTP {method}"

        with self.tracer.start_as_current_span(span_name, kind=trace.SpanKind.CLIENT) as span:
            # Set standard semantic conventions
            span.set_attribute("http.method", method)
            span.set_attribute("http.url", url)

            # Inject trace context headers (traceparent) into request if supported
            if hasattr(request, "headers") and isinstance(request.headers, dict):
                inject(request.headers)

            try:
                response = next_call(request)
                status_code = getattr(response, "status_code", 200)
                span.set_attribute("http.status_code", status_code)
                
                if status_code >= 400:
                    span.set_status(Status(StatusCode.ERROR, f"HTTP {status_code}"))
                else:
                    span.set_status(Status(StatusCode.OK))
                    
                return response

            except Exception as exc:
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR, str(exc)))
                raise