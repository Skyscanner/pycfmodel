SOURCES = $(shell find . -name "*.py")

install:
	uv sync --no-dev

install-dev:
	uv sync --all-extras

install-docs:
	uv sync --extra docs

install-cloudformation-update:
	uv sync --extra cloudformation-update

cloudformation-update:
	uv run python scripts/generate_cloudformation_actions_file.py

format: isort-format black-format

isort-format:
	uv run isort .

black-format:
	uv run black .

lint: isort-lint black-lint ruff-lint

isort-lint:
	uv run isort --check-only .

black-lint:
	uv run black --check .

ruff-lint:
	uv run ruff check .

unit:
	uv run pytest -svvv tests

coverage:
	uv run coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	uv run coverage report
	uv run coverage xml -i -o build/coverage.xml
	uv run coverage html

coverage-master:
	uv run coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v -m "not actions"
	uv run coverage report
	uv run coverage xml -i -o build/coverage.xml
	uv run coverage html

test: lint unit

test-docs:
	uv run mkdocs build --strict

lock:
	uv lock

lock-upgrade:
	uv lock --upgrade

.PHONY: install install-dev install-docs install-cloudformation-update format isort-format black-format lint isort-lint \
        black-lint ruff-lint unit coverage coverage-master test test-docs cloudformation-update lock lock-upgrade
