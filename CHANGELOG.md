# Changelog

All notable changes to this project will be documented in this file.

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