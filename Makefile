.PHONY: help install install-dev test test-cov lint format type-check pre-commit clean build docs
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e ".[dev,docs,jupyter]"

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=genome_matrix_mds --cov-report=html --cov-report=term-missing

lint: ## Run linting (ruff)
	ruff check src tests

lint-fix: ## Run linting with auto-fix
	ruff check --fix src tests

format: ## Format code (black)
	black src tests

format-check: ## Check code formatting
	black --check src tests

type-check: ## Run type checking (mypy)
	mypy src

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	python -m build

docs: ## Build documentation
	cd docs && make html

docs-clean: ## Clean documentation build
	cd docs && make clean

docs-live: ## Serve documentation with live reload
	cd docs && make livehtml

check-all: lint type-check test ## Run all checks (lint, type-check, test)

ci: check-all ## Run all CI checks

release-test: ## Build and test package for release
	python -m build
	python -m twine check dist/*

release: ## Release package to PyPI
	python -m build
	python -m twine upload dist/*

# Development shortcuts
dev-setup: install-dev pre-commit-install ## Setup development environment
	@echo "Development environment setup complete!"

dev-check: format lint type-check test ## Run development checks
	@echo "All development checks passed!"