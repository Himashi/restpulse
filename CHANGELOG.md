# Changelog

All notable changes to this project will be documented in this file.

## 11.0.0
### Added
- **OpenTelemetry & W3C Trace Context Propagation:** Updated `OpenTelemetryMiddleware` in `src/restpulse/middleware/opentelemetry.py` with full asynchronous support and W3C trace context injection (`traceparent` header propagation).
- **Distributed Tracing Integration:** Enhanced span attributes, status codes, and exception tracking to seamlessly integrate with enterprise APMs.
- **Testing:** Converted and updated test suite in `tests/test_opentelemetry.py` to verify asynchronous span creation, trace context headers, and telemetry export.

## 10.0.0
### Added
- **Smart Connection Pooling & Keep-Alive:** Introduced `ConnectionPoolConfig` in `src/restpulse/config.py` and integrated connection limits, socket reuse, and configurable keep-alive expirations into `RestPulseClient`.
- **Performance Optimization:** Minimized overhead under high-throughput enterprise load by enabling long-lived connection reuse instead of instantiating new clients per request.
- **Testing:** Added comprehensive test coverage in `tests/test_connection_pooling.py` to verify connection limits and timeout configurations.

## 9.0.0
### Added
- **Data Masking Middleware:** Introduced `DataMaskingMiddleware` in `restpulse.middleware` to automatically sanitize sensitive PII (such as passwords, tokens, SSNs, and credit card numbers) from request bodies, headers, and query payloads.
- **Compliance Support:** Helps ensure readiness for enterprise compliance standards like SOC2, GDPR, and HIPAA by preventing raw security leaks in payloads.
- **Testing:** Added comprehensive unit test coverage in `tests/test_data_masking.py` verifying header and JSON body sanitization.

## 8.0.0
### Added
- **Rate-Limiting Middleware:** Introduced `RateLimitMiddleware` in `restpulse.middleware` to provide client-side throttling and prevent overloading downstream microservices.
- **Throttling & Backoff:** Added support for configurable request limits, sliding time windows, exponential backoff, and automatic handling of `429 Too Many Requests` responses with `Retry-After` header parsing.
- **Testing:** Added unit test coverage in `tests/test_rate_limit.py` validating rate enforcement and retry/backoff mechanisms.

## 7.0.0
### Added
- **OpenTelemetry Middleware:** Introduced `OpenTelemetryMiddleware` in `restpulse.middleware` to automatically instrument outgoing requests with distributed tracing spans.
- **Trace Context Propagation:** Added W3C Trace Context header injection (`traceparent`, `tracestate`) to seamlessly track requests across microservice boundaries.
- **Testing:** Added comprehensive unit tests in `tests/test_opentelemetry.py` utilizing the OpenTelemetry in-memory span exporter to validate telemetry attributes and header propagation.

## 6.0.0

### Added
- **Circuit Breaker Middleware:** Introduced `CircuitBreakerMiddleware` in `restpulse.middleware` to prevent cascading network failures and fail fast when downstream services are unhealthy.
- **Resilience States:** Implemented standard circuit breaker states (`CLOSED`, `OPEN`, `HALF-OPEN`) with configurable failure thresholds and recovery timeouts, alongside `CircuitOpenError`.
- **Testing:** Added comprehensive unit tests in `tests/test_circuit_breaker.py` verifying state transitions and fast-fail behavior.

## 5.0.0

### Added
- **Telemetry Middleware:** Introduced `TelemetryMiddleware` in `restpulse.middleware` to automatically inject correlation IDs (`X-Request-ID`) for distributed tracing.
- **Observability:** Added request/response logging capturing precise round-trip latency (in milliseconds), HTTP methods, and status codes.
- **Testing:** Added comprehensive unit test coverage for telemetry middleware (`tests/test_telemetry.py`).

## 4.2.0

### Added
- **Multi-Stage CI/CD Pipeline:** Structured GitHub Actions workflow into 4 distinct sequential stages (`build`, `test`, `dev`, and `prod`) for automated builds, testing, and deployment.

## 4.1.0

### Added
- **Multi-Stage CI/CD Pipeline:** Configured sequential GitHub Actions pipeline stages (`test`, `deploy-staging`, and `deploy-production`) to automate testing and release workflows.

## 4.0.0

### Added
- **Custom Middleware & Global Hooks:** Introduced `before_request` and `after_response` lifecycle hook decorators to `RestPulseClient` for global request modification and response interception.
- **Unit Tests:** Added comprehensive test coverage for synchronous hook execution flow in `tests/test_middleware.py`.

## 3.2.0

### Added
- Automatic retry and exponential backoff strategy for transient 5xx errors and network/timeout failures in both sync and async clients.

## 3.1.0

### Added
- **Community Standards:** Added a comprehensive `CONTRIBUTING.md` guide to assist developers with environment setup, running tests, and submitting pull requests.
- **Open Source License:** Added the MIT License to give clear legal permissions for users and contributors.

## 3.0.0

### Added
- **Automatic Retries:** Added built-in retry logic with exponential backoff for synchronous and asynchronous requests to handle flaky network issues and temporary 5xx server errors.
- **Configurable Retry Parameters:** Introduced `retries` and `backoff_factor` configuration options in `RestPulseClient`.
- **Retry Unit Tests:** Added mock tests verifying successful recovery after initial server error responses.

## 2.0.0

### Added
- **Custom Exceptions:** Introduced a structured error hierarchy (`RestPulseError`, `APIError`, `NotFoundError`, `AuthenticationError`) for easier debugging and cleaner integration.
- **Automatic Error Translation:** Automatically intercepts `httpx.HTTPStatusError` and maps status codes (like `401 Unauthorized` and `404 Not Found`) to their respective custom exceptions.
- **Exception Unit Tests:** Added robust mock tests verifying that `NotFoundError` and `AuthenticationError` are raised correctly during sync and async requests.

## 1.0.0

### Added
- Core synchronous (`RestPulseClient.get`) and asynchronous (`RestPulseClient.get_async`) HTTP methods via `httpx`.
- Type-safe data validation and structuring via Pydantic models (`APIResponse`, `PulseData`).
- Built-in environment variable configuration support using `python-dotenv`.
- Unit testing suite utilizing `pytest`, `pytest-asyncio`, and `respx` for mock requests.
- Comprehensive initial documentation and `README.md`.