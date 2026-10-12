# API Reference

Complete reference for `restpulse` clients, configurations, and built-in middlewares.

---

## `RestPulseClient`

The primary HTTP client wrapper.

```python
from restpulse import RestPulseClient, ConnectionPoolConfig

client = RestPulseClient(
    base_url="[https://api.example.com](https://api.example.com)",
    pool_config=ConnectionPoolConfig(max_connections=50),
    middlewares=[...]
)
```

## Methods
- client.get(url, **kwargs): Synchronous GET request.

- client.get_async(url, **kwargs): Asynchronous GET request.

- client.post(url, json=None, **kwargs): Synchronous POST request.

- client.post_async(url, json=None, **kwargs): Asynchronous POST request.


**ConnectionPoolConfig**


Configuration object for smart connection pooling.

from restpulse import ConnectionPoolConfig

```
python

config = ConnectionPoolConfig(
    max_connections=100,             # Maximum concurrent connections
    max_keepalive_connections=20,    # Max idle connections kept alive in pool
    keepalive_expiry=5.0             # Time in seconds before idle sockets close
)
```
## Middlewares
**OpenTelemetryMiddleware**

Injects W3C trace context headers for distributed tracing.

```Python
from restpulse.middleware import OpenTelemetryMiddleware
middleware = OpenTelemetryMiddleware(service_name="my-service")
```

**DataMaskingMiddleware**

Redacts PII and sensitive tokens from request payloads and headers.

```python
from restpulse.middleware import DataMaskingMiddleware

middleware = DataMaskingMiddleware(mask_string="***REDACTED***")
```

**CircuitBreakerMiddleware**

Prevents cascading failures by short-circuiting failing downstream calls.

```
Python
from restpulse.middleware import CircuitBreakerMiddleware

middleware = CircuitBreakerMiddleware(failure_threshold=5, recovery_timeout=30)
```

**RateLimitMiddleware**

Throttles outbound requests to comply with API rate limits.

```
Python
from restpulse.middleware import RateLimitMiddleware

middleware = RateLimitMiddleware(max_requests=100, window_seconds=60)
```