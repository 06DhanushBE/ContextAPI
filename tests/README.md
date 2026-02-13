# Tests Directory

This directory contains all tests for the ContextAPI application.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests in verbose mode
pytest -v
```

## Test Structure

- `test_api.py` - API endpoint tests
- More test files to be added...

## Writing Tests

Tests use pytest framework. Follow these conventions:

- Test files should start with `test_`
- Test functions should start with `test_`
- Use descriptive test names
- Add docstrings to explain what each test does

## Coverage Goals

Target: 70%+ code coverage before production deployment.
