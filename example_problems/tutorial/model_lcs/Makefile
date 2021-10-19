PROBLEM_NAME=$(notdir $(shell pwd))
GEN_DIR = $(shell pwd)/gen/

gen-inputs:
	echo "Generating inputs directory..."
	./gen/TAL_gen.py $(GEN_DIR)

clean-all:
	echo "Removing gen_dictionary file..."
	rm -rf ./gen/gen_dictionary.txt
	echo "Removing inputs directory..."
	rm -rf inputs
	echo "Removing TMP_DIR directory..."
	rm -rf tmp97815
