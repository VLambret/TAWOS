RST=results

.PHONY: all clean

all:

clean :

.PHONY : test pytest integration_tests pylint coverage

test : pytest

pytest:
	PYTHONPATH=src py.test-3

coverage:
	PYTHONPATH=src py.test-3 --cov=src --cov-report term-missing

pylint:
	pylint --rcfile=pylintrc src/*.py src/*/*.py


