# Contributing to RestPulse

Thank you for your interest in contributing to `restpulse`! We appreciate all contributions, whether it's bug reports, feature requests, documentation improvements, or code pull requests.

## How to Contribute

1. **Fork the Repository** and clone your fork locally.
2. **Create a Feature Branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
3. **Set Up Your Development Environment:**
    - Install dependencies in editable mode:
    ```bash
    Bash

    pip install -e .[dev]
4. **Write Tests:**
    - Ensure any new features, middlewares, or bug fixes include unit tests.
    - Use pytest, anyio (for async tests), and respx (for mocking HTTP requests).

5. **Run the Test Suite:**
    - Verify all tests pass successfully:
    ```bash
    Bash

    pytest

6. **Commit Your Changes:**
    - Use conventional commit messages

    `(e.g., feat(middleware): add custom header support, fix: handle connection timeout).`

7. **Push and Submit a Pull Request:**
    - Push your branch to your fork and submit a Pull Request against the main branch.

## Development Guidelines
**Type Safety:**

 Ensure all new code uses Python type hints and passes static analysis.

**Middleware Design:**

 If adding new middleware, follow the async-first pattern (async def __call__) compatible with httpx.