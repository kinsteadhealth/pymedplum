.PHONY: help install install-dev install-pre-commit test test-unit test-integration lint format type-check check clean build publish

# Default target
help:
	@echo "PyMedplum Development Commands"
	@echo "================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install package dependencies"
	@echo "  make install-dev          Install package with dev dependencies"
	@echo "  make install-pre-commit   Install pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests with coverage"
	@echo "  make test-unit            Run unit tests only"
	@echo "  make test-integration     Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint                 Run ruff linter (with auto-fix)"
	@echo "  make format               Run ruff formatter"
	@echo "  make type-check           Run mypy type checker"
	@echo "  make check                Run all code quality checks"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                Remove build artifacts and cache"
	@echo "  make build                Build distribution packages"
	@echo "  make publish              Publish to PyPI (requires credentials)"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-pre-commit: install-dev
	pre-commit install
	@echo "Pre-commit hooks installed successfully!"

# Testing targets
test:
	python -m pytest

test-unit:
	python -m pytest pymedplum/tests/unit/

test-integration:
	python -m pytest pymedplum/tests/integration/

# Code quality targets
lint:
	python -m ruff check --fix .

format:
	python -m ruff format .

type-check:
	python -m mypy pymedplum/

check: lint format type-check
	@echo "All code quality checks passed!"

# Utility targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	find . -type f -name '.coverage' -delete
	find . -type f -name 'coverage.xml' -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*
