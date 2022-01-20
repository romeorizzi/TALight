PROBLEM_NAME=$(notdir $(shell pwd))
GEN_DIR = $(shell pwd)/gen/

gen-instances:
	echo "Generating the catalogue of the stored instances ..."
	./gen/TAL_make_catalogue.py $(GEN_DIR)

clean:
	echo "Removing the instances_catalogue directory..."
	rm -rf instances_catalogue
