# Contributing to RestPulse

Thank you for your interest in contributing to `restpulse`! We appreciate all contributions, whether it's bug reports, feature requests, documentation improvements, or code pull requests.

## How to Contribute

1. **Fork the Repository** and clone your fork locally.
2. **Create a Feature Branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name

**Set Up Your Development Environment:**

- **Install dependencies:** 
  ```bash
  pip install -e .[dev]

(or your preferred setup using poetry/pipenv).

- **Write Tests:**

Ensure any new features or bug fixes include unit tests using pytest and respx.

- **Run the Test Suite:**
  ```bash
  pytest
- Commit Your Changes: Use conventional commit messages (e.g., feat: add timeout configuration, fix: handle connection timeout).

- Push to Your Fork and submit a Pull Request to the main branch.
