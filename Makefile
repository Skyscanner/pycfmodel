SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt .

install-docs:
	pip install -r requirements.txt -r requirements-docs.txt .

format: isort-format black-format

isort-format:
	isort .

black-format:
	black .

lint: isort-lint black-lint ruff-lint

isort-lint:
	isort --check-only .

black-lint:
	black --check .

ruff-lint:
	ruff check .

unit:
	pytest -svvv tests

coverage:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml
	coverage html

coverage-master:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v -m "not actions"
	coverage report
	coverage xml -i -o build/coverage.xml
	coverage html

test: lint unit

test-docs:
	mkdocs build --strict

FREEZE_OPTIONS = --no-emit-index-url --no-annotate -v --resolver=backtracking
freeze-base:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml $(FREEZE_OPTIONS) --output-file requirements.txt
freeze-dev:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra dev $(FREEZE_OPTIONS) --output-file requirements-dev.txt
freeze-docs:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra docs $(FREEZE_OPTIONS) --output-file requirements-docs.txt

freeze: freeze-base freeze-dev freeze-docs

freeze-base-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml $(FREEZE_OPTIONS) --upgrade --output-file requirements.txt
freeze-dev-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra dev $(FREEZE_OPTIONS) --upgrade --output-file requirements-dev.txt
freeze-docs-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra docs $(FREEZE_OPTIONS) --upgrade --output-file requirements-docs.txt

freeze-upgrade: freeze-base-upgrade freeze-dev-upgrade freeze-docs-upgrade

.PHONY: install install-dev install-docs format isort-format black-format lint isort-lint black-lint flake8-lint unit \
        coverage test freeze freeze-upgrade freeze-base freeze-dev freeze-docs freeze-base-upgrade freeze-dev-upgrade \
        freeze-docs-upgrade
