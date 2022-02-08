blackify:
	poetry run black py_pdf_term tests scripts

build-docs: clean-docs
	poetry run sphinx-build docs build
	poetry run python docs/scripts/postprocess.py

clean-docs:
	rm -Rf build

format: isortify blackify

gen-test-coverage:
	poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=xml

isortify:
	poetry run isort --profile black py_pdf_term tests scripts

lint-fix:
	poetry run flake8 py_pdf_term tests scripts

poetryversion:
	poetry version $(version) 

publish-docs: build-docs
	poetry run ghp-import -p build

test:
	poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=term-missing

version: poetryversion
	$(eval NEW_VERSION := $(shell cat pyproject.toml | grep "^version = \"*\"" | cut -d'"' -f2))
	sed -i "" "s/__version__ = .*/__version__ = \"$(NEW_VERSION)\"/g" py_pdf_term/__init__.py
