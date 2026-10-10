# Changelog

All notable changes to this project will be documented in this file.

## 1.0.0

### Added
- Core synchronous (`RestPulseClient.get`) and asynchronous (`RestPulseClient.get_async`) HTTP methods via `httpx`.
- Type-safe data validation and structuring via Pydantic models (`APIResponse`, `PulseData`).
- Built-in environment variable configuration support using `python-dotenv`.
- Unit testing suite utilizing `pytest`, `pytest-asyncio`, and `respx` for mock requests.
- Comprehensive initial documentation and `README.md`.