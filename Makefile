SOURCES = $(shell find . -name "*.py")

install:
	PIP_CONFIG_FILE=pip.conf pip install -r requirements.txt

install-dev: install
	PIP_CONFIG_FILE=pip.conf pip install -e ".[dev]"

lint:
	flake8 pycfmodel/ # tests/

component:
	pytest -sv tests

coverage:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml

test: lint component

freeze:
	PIP_CONFIG_FILE=pip.conf pip-compile --output-file requirements.txt setup.py

.PHONY: install install-dev lint component coverage test freeze
