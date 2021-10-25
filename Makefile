build-docs:
	poetry run sphinx-build docs build
	poetry run python docs/scripts/postprocess.py

clean-build-docs: clean build

clean-docs:
	rm -Rf build

gen-test-coverage:
	poetry run poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=xml

publish-docs: clean build
	poetry run ghp-import -p build

test:
	poetry run poetry run pytest --cov=py_pdf_term --cov-branch --cov-report=term-missing
