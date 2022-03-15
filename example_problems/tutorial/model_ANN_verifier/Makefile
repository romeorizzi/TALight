PROBLEM_NAME=$(notdir $(shell pwd))
GEN_DIR = $(shell pwd)/gen/

gen-instances:
	echo "Generating instances directory..."
	./gen/TAL_make_catalogue.py $(GEN_DIR)

clean-all:
	echo "Removing instances directory..."
	rm -rf instances
	echo "Removing TMP_DIR directory..."
	rm -rf tmp97815

deliverables: pdf-files/statement.pdf

pdf-files/statement.pdf:
	if [ -e pdf-files/statement.tex ]; then \
		pdflatex -output-directory pdf-files pdf-files/statement.tex ; \
		pdflatex -output-directory pdf-files pdf-files/statement.tex ; \
		rm -rf pdf-files/statement.log pdf-files/statement.aux pdf-files/statement.out ; \
        else echo 'No file statement.pdf generated (since no file statement.tex found)'; \
        fi

test: test_ref_solutions test_services
	echo "target testing"
	rtalc
	if [ $? -ne 0 ]; then echo "rtalc encounters problems with the meta.yaml file"; fi

test_ref_solutions:
	echo "test_ref_solutions now tests that the reference solutions work as expected"

test_services:
	echo "test_services now tests that the services work as expected"
