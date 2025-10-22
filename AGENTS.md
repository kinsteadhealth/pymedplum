# Agent Instructions for PyMedplum

This document provides instructions for AI agents to contribute to the PyMedplum project.

## Development Environment

- Use `make install-dev` to install all dependencies, including development and testing tools.
- This project uses `ruff` for linting and formatting, and `mypy` for type checking.

## Testing

- Run all tests with `make test`.
- Run unit tests only with `make test-unit`.
- Run integration tests only with `make test-integration`.
- Make sure all tests pass before submitting a pull request.

### Integration Tests

- Integration tests require a running Medplum server.
- You must create a `.env` file in the root of the project with the following variables:
  - `MEDPLUM_BASE_URL`
  - `MEDPLUM_CLIENT_ID`
  - `MEDPLUM_CLIENT_SECRET`
- The `passenv` configuration in `tox.ini` will make these environment variables available to the integration tests.

## Code Quality

- Run `make check` to run all code quality checks, including linting, formatting, and type checking.
- Run `make lint` to automatically fix linting issues.
- Run `make format` to format the code.
- Run `make type-check` to run the type checker.

## Pull Requests

- Before submitting a pull request, please run `make check` and `make test`.
- Ensure your PR title and description are clear and concise.
- If your PR addresses an issue, please reference the issue number in the description.

## Coding Style

- Follow the existing coding style.
- Use type hints for all function signatures.
- Keep functions small and focused on a single task.
- Add comments to explain complex logic.
- When adding new features, please also add corresponding tests.
