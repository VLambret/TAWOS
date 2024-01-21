RST=results

.PHONY: all clean

all: all_projects

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


################################################################################
# COMPUTE METRICS
################################################################################

PROJECT_FILES := $(wildcard projects/*)
DONE_FILES := $(patsubst projects/%, projects/.%.done, $(PROJECT_FILES))

#all_projects : $(DONE_FILES)
all_projects : projects/.Spring_XD.done

projects/.%.done: projects/%
	@echo $<



