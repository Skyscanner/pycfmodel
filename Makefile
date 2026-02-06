SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt .

install-docs:
	pip install -r requirements.txt -r requirements-docs.txt .

install-cloudformation-update:
	pip install -r requirements-cloudformation-update.txt .

cloudformation-update:
	python3 scripts/generate_cloudformation_actions_file.py

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
freeze-cloudformation-update:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra cloudformation-update $(FREEZE_OPTIONS) --output-file requirements-cloudformation-update.txt

freeze: freeze-base freeze-dev freeze-docs freeze-cloudformation-update

freeze-base-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml $(FREEZE_OPTIONS) --upgrade --output-file requirements.txt
freeze-dev-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra dev $(FREEZE_OPTIONS) --upgrade --output-file requirements-dev.txt
freeze-docs-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra docs $(FREEZE_OPTIONS) --upgrade --output-file requirements-docs.txt
freeze-cloudformation-update-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile pyproject.toml --extra cloudformation-update $(FREEZE_OPTIONS) --upgrade --output-file requirements-cloudformation-update.txt

freeze-upgrade: freeze-base-upgrade freeze-dev-upgrade freeze-docs-upgrade freeze-cloudformation-update-upgrade

.PHONY: install install-dev install-docs install-cloudformation-update format isort-format black-format lint isort-lint \
        black-lint flake8-lint unit coverage test cloudformation-update freeze freeze-upgrade freeze-base freeze-dev \
        freeze-docs freeze-cloudformation-update freeze-base-upgrade freeze-dev-upgrade freeze-docs-upgrade \
        freeze-cloudformation-update-upgrade
