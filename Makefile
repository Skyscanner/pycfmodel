install:
	uv sync --no-dev --locked

install-dev:
	uv sync --all-extras --locked

install-docs:
	uv sync --extra docs --locked

install-cloudformation-update:
	uv sync --extra cloudformation-update --locked

cloudformation-update:
	uv run --locked python scripts/generate_cloudformation_actions_file.py

fix:
	uv run --locked ruff check --fix .

format:
	uv run --locked isort .
	uv run --locked black .

lint:
	uv run --locked isort --check-only .
	uv run --locked black --check .
	uv run --locked ruff check .

unit:
	uv run --locked pytest -svvv tests

coverage:
	uv run --locked coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	uv run --locked coverage report
	uv run --locked coverage xml -i -o build/coverage.xml
	uv run --locked coverage html

coverage-master:
	uv run --locked coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v -m "not actions"
	uv run --locked coverage report
	uv run --locked coverage xml -i -o build/coverage.xml
	uv run --locked coverage html

coverage-html:
	uv run --locked coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	uv run --locked coverage html
	open htmlcov/index.html

test: lint unit

test-docs:
	uv run --locked mkdocs build --strict

lock:
	uv lock --default-index https://pypi.org/simple

lock-upgrade:
	uv lock --upgrade --default-index https://pypi.org/simple

.PHONY: install install-dev install-docs install-cloudformation-update cloudformation-update \
        fix format lint unit coverage coverage-master coverage-html test test-docs lock lock-upgrade
