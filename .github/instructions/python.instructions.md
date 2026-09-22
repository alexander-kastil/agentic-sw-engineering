---
name: Python Coding Conventions
description: This file describes the Python coding conventions for the project
---

## Standards

- **Python Version**: 3.11 or later (3.10+ for legacy projects)
- **Package Management**: Use `pyproject.toml` with PEP 518 build system specification
- **Dependency Management**: Pin major versions in `pyproject.toml`; use `requirements.txt` only for tools/utilities
- **Virtual Environments**: Use `.venv` folder for virtual environments

## Code Style

- **Naming Conventions**:
  - `snake_case` for functions, variables, and module names
  - `PascalCase` for class names
  - `UPPERCASE` for constants
  - Prefix private attributes with single underscore: `_private_attribute`

- **Type Hints**: Use type hints for all function parameters and return types using Python 3.10+ syntax

  ```python
  def process_data(items: list[str], count: int = 10) -> dict[str, int]:
      pass
  ```

- **Docstrings**: Use module-level and class/function docstrings

  ```python
  """
  Module description explaining purpose and key components.
  """

  class MyClass:
      """Summary line. Extended description if needed."""
      pass
  ```

## Async/Await

- Use `async`/`await` for I/O-bound operations (API calls, file operations, database queries)
- Use `asyncio` for managing coroutines and async operations
- Always use `async with` for resource management in async contexts

## Environment Variables

- Use `python-dotenv` for loading environment variables from `.env` files
- Always check for missing required environment variables and provide helpful error messages
- Load dotenv at module initialization: `load_dotenv()`

## Project Structure

- Place imports at the top of the file in order: standard library, third-party, local
- Use relative imports for packages within the project: `from .module import function`
- Organize code into logical modules by responsibility, not by type

## Testing

- Use `pytest` for unit testing
- Use `pytest-asyncio` for async test fixtures
- Keep test files alongside or in `tests/` directory with `test_*.py` naming convention

## Package Specifications

- Use `pyproject.toml` for all project metadata and dependencies:
  - `[project]` section for name, version, description, requires-python, dependencies
  - `[build-system]` section with `hatchling` as build backend
  - Use `>=` for minimum versions; pin exact versions for critical dependencies

## CLI Tools

- Use `uv` for fast Python package and script management when available
- Use `python -m pip` for standard pip operations

## No Comments

- Write self-documenting code with clear names and structure
- Use docstrings for non-obvious logic only
- Avoid inline comments explaining obvious code
