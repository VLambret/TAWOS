RST=results

.PHONY: all clean

all: all_projects

clean : clean_projects

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
	mypy --check-untyped-defs src


################################################################################
# COMPUTE METRICS
################################################################################

CSV_FILES := $(wildcard projects/*/*.csv)
DONE_FILES := $(addsuffix .done, $(CSV_FILES))

all_projects : $(DONE_FILES)

clean_projects:
	rm -f projects/*/*.png
	rm -f projects/*/*.csv.done

%.csv.done: %.csv
	python3 src/main.py $<
	touch $@

metrics:
	python3 src/merge_mmre_quality_json_files.py projects/*/*.json




