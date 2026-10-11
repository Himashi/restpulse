# RestPulse 🚀

> A lightweight, type-safe Python REST API client wrapper supporting both synchronous and asynchronous workflows.

---

## Features

- **Sync & Async Support**: Built on top of `httpx` for flexible HTTP request handling.
- **Data Validation**: Powered by `pydantic` models for structured, type-safe responses.
- **Environment Driven**: Automatic configuration support via `.env` files using `python-dotenv`.
- **Developer Friendly**: Fully typed with Python annotations for clean IDE autocompletion.
- **Automatic Retries**: Built-in exponential backoff retry logic for transient server errors and network failures.
- **Custom Middleware & Global Hooks**: Intercept and modify requests/responses globally using `before_request` and `after_response` lifecycle hook decorators.

---

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone [https://github.com/Himashi/restpulse.git](https://github.com/Himashi/restpulse.git)
cd restpulse
pip install -e .[dev]
```

---

## Environment Setup

Create a `.env` file in your project root to set default client configurations:

```env
RESTPULSE_BASE_URL=[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)
RESTPULSE_API_KEY=your_optional_api_key
```

---

## Quickstart Usage

### Synchronous Request

```python
from restpulse import RestPulseClient

client = RestPulseClient(base_url="[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)")
response = client.get("/todos/1")

print(f"Status: {response.status_code}")
print(f"Data: {response.data}")
```

### Asynchronous Request

```python
import asyncio
from restpulse import RestPulseClient

async def main():
    client = RestPulseClient(base_url="[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)")
    response = await client.get_async("/todos/1")
    print(f"Async Response: {response.data}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Middleware & Global Hooks
You can register global hooks to automatically inject headers (like authorization tokens) or log request metrics across all calls:

```python
from restpulse import RestPulseClient

client = RestPulseClient(base_url="[https://api.example.com](https://api.example.com)")

# Auto-inject auth header before every request
@client.before_request
def add_auth(req):
    req["headers"]["Authorization"] = "Bearer your_token_here"
    return req

# Log response metadata after every request
@client.after_response
def log_metrics(response):
    print(f"[{response.status_code}] {response.url} took {response.elapsed_time:.3f}s")
    return response

response = client.get("/users")
```

---

## Running Tests

Run the test suite using `pytest`:

```bash
pytest
```

---

## License

This project is licensed under the [MIT License](LICENSE).