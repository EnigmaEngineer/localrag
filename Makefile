.PHONY: help install dev run test lint clean docker

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

dev: ## Install all dependencies (production + dev)
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

run: ## Start the API server
	python -m localrag.api.main

test: ## Run tests
	pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=localrag --cov-report=html

lint: ## Run linting
	ruff check localrag/ tests/
	ruff format --check localrag/ tests/
	mypy localrag/

format: ## Auto-format code
	ruff check --fix localrag/ tests/
	ruff format localrag/ tests/

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache htmlcov .coverage .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

docker: ## Build and run with Docker Compose
	docker compose up --build
