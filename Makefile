SOURCES = $(shell find . -name "*.py")

install:
	pip install -r requirements.txt

install-dev: install
	pip install -e ".[dev]"

install-docs:
	pip install -e ".[dev,docs]"

format:
	black .

lint:
	black --check .
	flake8 pycfmodel/ # tests/

component:
	pytest -sv tests

coverage:
	coverage run --source=pycfmodel --branch -m pytest tests/ --junitxml=build/test.xml -v
	coverage report
	coverage xml -i -o build/coverage.xml

test: lint component

freeze:
	CUSTOM_COMPILE_COMMAND="make freeze" PIP_CONFIG_FILE=pip.conf pip-compile --no-index --output-file requirements.txt setup.py

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze-upgrade" pip-compile --no-index --upgrade --output-file requirements.txt setup.py

.PHONY: install install-dev install-docs lint component coverage test freeze freeze-upgrade format
