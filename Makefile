.PHONY: default

default: build

.PHONY: clean

clean:
	rm -Rf ./build ./dist ./*.egg-info

.PHONY: build

build:
	python3 setup.py sdist bdist_wheel

.PHONY: publish

publish:
	python3 -m twine upload dist/*
