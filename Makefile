clean_build: clean build

build:
	poetry run sphinx-build docs build
	poetry run python docs/scripts/postprocess.py

clean:
	rm -Rf build

.PHONY: clean_build build clean
