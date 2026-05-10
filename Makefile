.PHONY: help install test clean run analyze lint format docs build

help:
	@echo "Hotel Data Analysis - Development Commands"
	@echo "==========================================="
	@echo ""
	@echo "Environment Setup:"
	@echo "  make install              Install all dependencies"
	@echo "  make install-dev          Install with development tools"
	@echo ""
	@echo "Running Analysis:"
	@echo "  make run                  Run data cleaning pipeline"
	@echo "  make analyze              Run analysis notebooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make test                 Run unit tests with coverage"
	@echo "  make lint                 Run code linters (Flake8, Pylint)"
	@echo "  make type-check           Run type checking (MyPy)"
	@echo "  make format               Format code with Black"
	@echo "  make format-check         Check formatting without changes"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean                Remove build artifacts"
	@echo "  make clean-data           Remove processed data"
	@echo "  make docs                 Generate documentation"
	@echo ""
	@echo "Deployment:"
	@echo "  make build                Build package"
	@echo "  make validate             Validate project structure"

# Environment Setup
install:
	pip install --upgrade pip
	pip install -e .

install-dev:
	pip install --upgrade pip
	pip install -e ".[dev]"

# Running Analysis
run:
	python scripts/clean_data.py --input data/raw/hotels.csv --output data/processed/cleaned_hotels.csv
	@echo "✓ Data cleaning complete"

analyze:
	@echo "Generating analysis notebooks..."
	jupyter nbconvert --to notebook --execute notebooks/01_data_exploration.ipynb
	jupyter nbconvert --to notebook --execute notebooks/02_analysis.ipynb
	@echo "✓ Analysis complete"

# Code Quality
test:
	pytest tests/ -v --cov=scripts --cov-report=html --cov-report=term-missing

test-fast:
	pytest tests/ -q

lint:
	flake8 scripts/ tests/ --max-line-length=127 --statistics
	pylint scripts/ --disable=R,C,W --exit-zero

type-check:
	mypy scripts/ --ignore-missing-imports --exit-zero || true

format:
	black scripts/ tests/
	isort scripts/ tests/

format-check:
	black --check scripts/ tests/ || true
	isort --check-only scripts/ tests/ || true

# Maintenance
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf htmlcov/
	rm -f .coverage
	@echo "✓ Cleaned build artifacts"

clean-data:
	rm -rf data/processed/*
	@echo "✓ Cleaned processed data"

docs:
	@echo "Documentation:"
	@echo "  - README.md (project overview)"
	@echo "  - docs/data_dictionary.md (schema)"
	@echo "  - docs/LEGAL.md (compliance)"
	@echo "  - docs/findings.md (analysis results)"
	@echo "  - CONTRIBUTING.md (development)"

# Deployment
build:
	python setup.py sdist bdist_wheel
	@echo "✓ Package built"

validate:
	@echo "Validating project structure..."
	@test -f LICENSE || (echo "ERROR: LICENSE file missing"; exit 1)
	@test -f setup.py || (echo "ERROR: setup.py missing"; exit 1)
	@test -f requirements.txt || (echo "ERROR: requirements.txt missing"; exit 1)
	@test -d scripts || (echo "ERROR: scripts/ directory missing"; exit 1)
	@test -d tests || (echo "ERROR: tests/ directory missing"; exit 1)
	@test -d docs || (echo "ERROR: docs/ directory missing"; exit 1)
	@test -f CONTRIBUTING.md || (echo "ERROR: CONTRIBUTING.md missing"; exit 1)
	@echo "✓ Project structure is valid"

# Combined workflows
all: clean install test lint format
	@echo "✓ Full pipeline complete"

ci: format-check lint test
	@echo "✓ CI pipeline passed"

full-setup: install-dev test lint format validate
	@echo "✓ Full project setup complete"
