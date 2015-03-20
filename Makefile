.PHONY: default test

default: test

test:
	python -m unittest discover
