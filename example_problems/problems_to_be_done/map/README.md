# LIST OF FILES IN THIS FOLDER (MAIN DIRECTORY FOR THIS PROBLEM)

## ALMOST-REQUIRED (SOURCE) FILES AND SUBFOLDERS FOR A PROBLEM TO BE COMPLETE TO GO:

evaluator.py
instance-generators
Makefile
makeInputs-suite.py
makeOutputs.sh
models
reference-outputs-generators
statement.md
Turingfile


## OPTIONAL FILES AND SUBFOLDERS FOR A PROBLEM TO BE COMPLETE TO GO:

examples
figs
makeInputs-extra.py
pdf-files

## OTHER SOURCE FILES OR FOLDERS:

README.md
old_stuff_with_CMS

## AUTOMATICALLY GENERATED FOLDERS 

inputs-suite.dat
inputs-suite.txt  (optional)
inputs-extra.dat (optional)
inputs-extra.txt (optional)
outputs-suite.txt
outputs-extra.txt (optional)
public (to offer materials even before the very first evaluation)
turingarena-files (when the problem is compiled in order to be served from the cloud)
generated-files (can appear after an evaluation in local has been called for) 

# USE OF THE MAKEFILE

make server (or just make): produces all files needed in order to serve the problem from a TuringArena cloud service (TuringArena is open source and you can easily set-up such a service if you have e server. If you agree to share your problem as an open-souce problem on GitHub, you can easily trigger that your problem be served from our service in the cloud, or ask us to do so for you). We regard a problem as a form of valuable content, but our commitment and vision is also to promote the sharing of problems and the collaborative design of didactical paths and experiences articulated in interactive problems. A well-designed problem, like a Montessori game, can teach better than a perfect essay on a subject.

make localtest: prepares all files required to test a solution model in local. Once this generation is complete, it also executes the evaluation of a default solution model.

make core: prepares all files required to test in local any solution model of your choice, or other additions. customizations or improvements you are working at.

make inputs: will generate the testcases (input_*.dat) files for the inputs-suite folder. This folder contains the testcases for testing the solutions submitted to the online evalution service.

make clean-inputs: deletes the folders inputs-suite.dat and inputs-suite.txt (all the ones which are present).

make inputs-extra, make clean-inputs-extra: the same as for inputs, but these extra inputs are only meant to be made available to the self-organizing student in a .zip archive, not used/served by the local or online verification service for providing validation, evaluation, feedback and general guidance to the student. These might be large instances requiring a lot of computational time.

make outputs, make clean-outputs, make outputs-extra, make clean-outputs-extra: every testcase comprises of an (input, output) pair. The input is the description of a specific instance of the problem/model, the output is the intended answer. Though the correct answer is not always unique, for each input in inputs-suite.*/* or inputs-extra.*/* we store in outputs.*/* or outputs-extra.*/* the corresponding reference oputput. As such, make outputs, make clean-outputs, make outputs-extra, make clean-outputs-extra correspond perfectly to make inputs, make clean-inputs, make inputs-extra, make clean-inputs-extra.

make all-inputs: inputs + inputs-extra

make all-outputs: outputs + outputs-extra

make clean-all-inputs, make clean-all-outputs: delete what the above generate

make all-instances: make all-inputs + make all-outputs

make clean-all-instances: make clean-all-inputs + make clean-all-outputs

make public: generates all files which go in the directory output. All the files contained in this directory are made available to the problem-solver facing the problem from the very start (even before her very first submission and solution attempts). Our suggestion is to make available in public at least one suite of testcases. If you do not implement an incremental accessibility mechanism to the hints and discussion materials, then you better include here also your solution models as reference.
What in the following directories goes here: gallery_of_models, inputs-suite, outputs-suite, extra-inputs, extra-outputs.

make pdf: generates the pdf files with the statement of the problem or other presentation material.

make clean: deletes all the automatically generated files or other temporary files.
