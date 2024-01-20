RST=results

.PHONY: all clean

all:

clean :

.PHONY : test pytest pylint coverage mypy

test : pytest

pytest:
	PYTHONPATH=src py.test-3

coverage:
	PYTHONPATH=src py.test-3 --cov=src --cov-report term-missing

pylint:
	pylint --rcfile=pylintrc src/*.py src/*/*.py

install_dependencies:
	pip install -r requirements.txt

mypy:
	mypy src


