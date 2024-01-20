RST=results

.PHONY: all clean

all:

clean :

.PHONY : test pytest integration_tests pylint coverage

test : pytest

pytest:
	py.test-3

coverage:
	py.test-3 --cov=src --cov-report term-missing

pylint:
	pylint --rcfile=pylintrc src/*.py
