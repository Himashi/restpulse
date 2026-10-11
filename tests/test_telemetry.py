import logging
from restpulse.middleware import TelemetryMiddleware

class MockRequest:
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.headers = {}

class DummyResponse:
    status_code = 200

def test_telemetry_middleware_success(caplog):
    caplog.set_level(logging.INFO)
    middleware = TelemetryMiddleware()
    
    req = MockRequest("GET", "https://api.example.com/data")
    
    def dummy_next(r):
        return DummyResponse()

    response = middleware(req, dummy_next)

    assert "X-Request-ID" in req.headers
    assert response.status_code == 200
    assert "Started request" in caplog.text
    assert "Completed request" in caplog.text