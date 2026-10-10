# Changelog

All notable changes to this project will be documented in this file.

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