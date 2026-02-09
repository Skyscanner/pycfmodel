install:
	uv sync --no-dev --frozen

install-dev:
	uv sync --all-extras --frozen

install-docs:
	uv sync --extra docs --frozen

install-cloudformation-update:
	uv sync --extra cloudformation-update --frozen

cloudformation-update:
	uv run --frozen python scripts/generate_cloudformation_actions_file.py

fix:
	uv run --frozen ruff check --fix .

format:
	uv run --frozen isort .
	uv run --frozen black .

lint:
	uv run --frozen isort --check-only .
	uv run --frozen black --check .
	uv run --frozen ruff check .

unit:
	uv run --frozen pytest -svvv tests

coverage:
	uv run --frozen coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	uv run --frozen coverage report
	uv run --frozen coverage xml -i -o build/coverage.xml
	uv run --frozen coverage html

coverage-html:
	uv run --frozen coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	uv run --frozen coverage html
	open htmlcov/index.html

test: lint unit

test-docs:
	uv run --frozen mkdocs build --strict

lock:
	uv lock --default-index https://pypi.org/simple

lock-upgrade:
	uv lock --upgrade --default-index https://pypi.org/simple

.PHONY: install install-dev install-docs install-cloudformation-update cloudformation-update \
        fix format lint unit coverage coverage-html test test-docs lock lock-upgrade
