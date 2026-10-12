# RestPulse 🚀

> The resilient, secure, and high-performance Python HTTP client for enterprise-grade applications. Built on top of `httpx`.

---

## Features

- **Sync & Async Support**: Built on top of `httpx` for flexible HTTP request handling across synchronous and asynchronous workflows.
- **Smart Connection Pooling**: Configurable connection limits, keep-alive timeouts, and socket reuse for high-throughput enterprise performance.
- **Distributed Tracing (OpenTelemetry)**: Native W3C trace context propagation (`traceparent`) for seamless tracing across microservices and enterprise APMs (Datadog, Jaeger, New Relic).
- **PII Data Masking**: Automatic sanitization and redaction of sensitive data (credentials, credit cards, PII) to support **SOC2, GDPR, and HIPAA compliance**.
- **Traffic Control & Rate Limiting**: Sliding window rate-limiting and automated `Retry-After` handling to prevent 429 throttling.
- **Circuit Breaker & Retries**: Automated exponential backoff and circuit breaking to prevent cascading failures during downstream outages.
- **Data Validation**: Powered by `pydantic` models for structured, type-safe responses.

---

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone [https://github.com/Himashi/restpulse.git](https://github.com/Himashi/restpulse.git)
cd restpulse
pip install -e .[dev]
```

Environment Setup

Create a .env file in your project root to set default client configurations:
```bash
RESTPULSE_BASE_URL=[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)
RESTPULSE_API_KEY=your_optional_api_key
```

Quickstart Usage

Asynchronous Request with Enterprise Features
```bash
python

import asyncio
from restpulse import RestPulseClient, ConnectionPoolConfig
from restpulse.middleware import (
    OpenTelemetryMiddleware,
    DataMaskingMiddleware,
    CircuitBreakerMiddleware,
    RateLimitMiddleware
)

async def main():
    # 1. Configure Connection Pooling
    pool_config = ConnectionPoolConfig(
        max_connections=50,
        max_keepalive_connections=10,
        keepalive_expiry=5.0
    )

    # 2. Initialize Client with Enterprise Middlewares
    client = RestPulseClient(
        base_url="[https://api.example.com](https://api.example.com)",
        pool_config=pool_config,
        middlewares=[
            OpenTelemetryMiddleware(),
            DataMaskingMiddleware(),
            RateLimitMiddleware(max_requests=100, window_seconds=60),
            CircuitBreakerMiddleware(failure_threshold=5)
        ]
    )

    # 3. Execute Async Request
    response = await client.get_async("/todos/1")
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")

if __name__ == "__main__":
    asyncio.run(main())
```
Synchronous Basic Request
```bash
python

from restpulse import RestPulseClient

client = RestPulseClient(base_url="[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)")
response = client.get("/todos/1")

print(f"Status: {response.status_code}")
print(f"Data: {response.data}")
```

##  Running Tests

Run the full test suite using pytest:
```bash
pytest
```
## Contributing

We welcome contributions! Please check out our CONTRIBUTING.md guide for details on our development workflow and testing standards.

##  License
This project is licensed under the MIT License.
