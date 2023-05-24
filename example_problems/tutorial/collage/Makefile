PROBLEM_HOME=$(shell pwd)
PROBLEM_NAME=$(notdir $(PROBLEM_HOME))
GEN_DIR=$(PROBLEM_HOME)/gen/

.PHONY: all
all: instances_catalogue test

instances_catalogue: $(GEN_DIR)GEN $(GEN_DIR)randgen_1_basic.py $(GEN_DIR)TAL_make_catalogue.py 
	@echo "Generating the catalogue of the stored instances ..."
	python $(GEN_DIR)TAL_make_catalogue.py $(GEN_DIR)

.PHONY: clean
clean:
	@if [ -e instances_catalogue ]; then \
		echo "Removing the instances_catalogue directory ..." ; \
		rm -rf instances_catalogue ; \
	fi
	@if [ -e services/__pycache__ ]; then \
		echo "Cleaning the cache ..." ; \
		rm -r services/__pycache__ ; \
	fi
	@if [ -e output ]; then echo "***THIS IS LET TO YOU: Consider removing the output folder"; fi
	@if [ -n "$(shell find . -maxdepth 1 -name 'my_*' | head ..." ; ]; then \
		echo "***THIS IS LET TO YOU: Consider removing some or all of the following folders whose names comply the template 'my_*'" ; \
		find . -maxdepth 1 -name 'my_*' ; \
	fi

.PHONY: lint
lint: $(shell find services -type f -name '*.py')
	pylint $?

.PHONY: test
test: test_metafile test_ref_solutions test_services

.PHONY: test_metafile
test_metafile: meta.yaml
	@echo "[test_metafile: now we test the metafile meta.yaml:"
	rtalc $(PROBLEM_HOME)
	@if [ $$? -ne 0 ]; then echo "rtalc encounters problems with the meta.yaml file"; fi
	@echo "OK test_metafile]\n"

.PHONY: test_ref_solutions
test_ref_solutions:
	@echo "[test_ref_solutions: now we test that the reference solutions work as expected"
	@echo "OK test_ref_solutions]\n"

.PHONY: test_services
test_services:
	@echo "[test_services: now we test that the services work as expected"
	@echo "OK test_services]\n"
