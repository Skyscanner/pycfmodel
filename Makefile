SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

format:
	black --exclude venv/ .

lint:
	black --check --exclude venv/ .
	flake8 pycfmodel/ # tests/

component:
	pytest -sv tests

coverage:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml

test: lint component

freeze:
	PIP_CONFIG_FILE=pip.conf pip-compile --no-index --output-file requirements.txt setup.py

.PHONY: install install-dev lint component coverage test freeze format
