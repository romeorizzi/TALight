PROBLEM_NAME=$(notdir $(shell pwd))
GEN_DIR = $(shell pwd)/gen/

gen-instances:
	echo "Generating instances directory..."
	./gen/TAL_make_catalogue.py $(GEN_DIR)

clean:
	echo "Removing instances directory..."
	rm -rf instances
	echo "Removing TMP_DIR directory..."
	rm -rf tmp97815
