PROBLEM_NAME=$(notdir $(shell pwd))
REF_SOLUTION=models/$(PROBLEM_NAME)_ref-eval-model.mod

server: core
	turingarena-dev file sync --zip --force

localtest: core
	turingarena-dev evaluate  --store-files $(REF_SOLUTION)

core: all-instances public

all-instances: all-inputs all-outputs

all-instances-full: all-inputs-full all-outputs-full

all-inputs: inputs inputs-extra

all-outputs: outputs outputs-extra

all-inputs-full: all-inputs inputs-txt inputs-extra-txt

inputs:
	./makeInputs-suite.py inputs-suite.dat dat

inputs-extra:
	./makeInputs-extra.py inputs-extra.dat dat

inputs-txt:
	./makeInputs-suite.py inputs-suite.txt txt

inputs-extra-txt:
	./makeInputs-extra.py inputs-extra.txt txt

outputs:
	./makeOutputs.sh inputs-suite.dat outputs-suite.txt dat txt

outputs-extra:
	./makeOutputs.sh inputs-extra.dat outputs-extra.txt dat txt

public: pdf
	echo Making up of the public directory
	rm -rf public
	mkdir public
	cp pdf-files/statement.pdf public/
	cp inputs-suite.dat/input_1.dat public/
	rm -rf testcases
	mkdir testcases
	cp inputs-suite.dat/* testcases/
	cp outputs-suite.txt/* testcases/
	zip -r public/testcases.zip testcases
	rm -rf testcases
	rm -rf testcases-extra
	mkdir testcases-extra
	cp inputs-extra.dat/* testcases-extra/
	cp outputs-extra.txt/* testcases-extra/
	zip -r public/testcases-extra.zip testcases-extra
	rm -rf testcases-extra
#	cp -r figs public/
#	zip public/gallery_of_models.zip models/gallery_of_models

pdf: pdf-files/statement.pdf

pdf-files/statement.pdf:
	if [ -e pdf-files/statement.tex ]; then \
		pdflatex -output-directory pdf-files pdf-files/statement.tex ; \
		pdflatex -output-directory pdf-files pdf-files/statement.tex ; \
		rm -rf pdf-files/statement.log pdf-files/statement.aux pdf-files/statement.out ; \
        else echo 'No file statement.pdf generated (since no file statement.tex found)'; \
        fi


examples/input_1.dat:
examples/input_1.txt:
outputs-suite.txt/output_1.txt:
models/gallery_of_models:

clean-inputs:
	rm -rf inputs-suite.dat inputs-suite.txt

clean-inputs-extra:
	rm -rf inputs-extra.dat inputs-extra.txt

clean-outputs:
	rm -rf outputs-suite.txt outputs-suite.dat

clean-outputs-extra:
	rm -rf outputs-extra.txt outputs-extra.dat

clean-all-inputs: clean-inputs clean-inputs-extra

clean-all-outputs: clean-outputs clean-outputs-extra

clean-all-instances: clean-all-inputs clean-all-outputs

clean: clean-all-instances
	rm -rf public generated-files turingarena-files *.zip
	find -iname '*.bin' -print0 | xargs -0 rm -f
	find -iname '*.pyc' -print0 | xargs -0 rm -f
	find -iname '*.jar' -print0 | xargs -0 rm -f
	find -iname '*.o' -print0 | xargs -0 rm -f
	find -iname '*~' -print0 | xargs -0 rm -f
	find -iname '*.bak' -print0 | xargs -0 rm -f
	find -iname '*.log' -print0 | xargs -0 rm -f
	find -iname '*.aux' -print0 | xargs -0 rm -f
	find -iname '*.out' -print0 | xargs -0 rm -f

