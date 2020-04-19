SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

install-docs:
	pip install -e ".[dev,docs]"

format: isort-format black-format

isort-format:
	isort --recursive .

black-format:
	black .

lint: isort-lint black-lint flake8-lint

isort-lint:
	isort --check-only --recursive .

black-lint:
	black --check .

flake8-lint:
	flake8 .

unit:
	pytest -svvv tests

coverage:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml
	coverage html

test: lint unit

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile --no-index --output-file requirements.txt setup.py

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze-upgrade" pip-compile --no-index --upgrade --output-file requirements.txt setup.py

.PHONY: install install-dev install-docs format isort-format black-format lint isort-lint black-lint flake8-lint unit coverage test freeze freeze-upgrade