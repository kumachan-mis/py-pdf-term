build-docs: clean-docs
	poetry run sphinx-build docs build
	poetry run python docs/scripts/postprocess.py

clean-docs:
	rm -Rf build

format:
	poetry run isort --profile black py_pdf_term tests scripts
	poetry run black py_pdf_term tests scripts

gen-test-coverage:
	poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=xml

lint-fix:
	poetry run flake8 py_pdf_term tests scripts

publish-docs: build-docs
	poetry run ghp-import -p build

test:
	poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=term-missing
