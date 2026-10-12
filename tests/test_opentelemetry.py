from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from restpulse.middleware.opentelemetry import OpenTelemetryMiddleware

class MockRequest:
    def __init__(self, method="GET", url="https://api.example.com"):
        self.method = method
        self.url = url
        self.headers = {}

class MockResponse:
    status_code = 200

def test_opentelemetry_middleware_creates_span():
    # Setup in-memory OTel exporter for test verification
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("test-tracer")

    middleware = OpenTelemetryMiddleware(tracer_instance=tracer)
    req = MockRequest()

    response = middleware(req, lambda r: MockResponse())

    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == "HTTP GET"
    assert spans[0].attributes["http.method"] == "GET"
    assert spans[0].attributes["http.status_code"] == 200
    assert "traceparent" in req.headers