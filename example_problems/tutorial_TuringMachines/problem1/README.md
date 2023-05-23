# LIST OF FILES AND SUBFOLDER IN THIS FOLDER (MAIN DIRECTORY FOR THIS PROBLEM)
public (to offer materials through rtal get)

## AUTOMATICALLY GENERATED FOLDERS 

inputs

# USE OF THE MAKEFILE

make server (or just make): produces all files needed in order to serve the problem from a TALight cloud server (TALight is open source and you can easily set-up such a service if you have a server. If you agree to share your problem as an open-souce problem on GitHub, you can easily trigger that your problem be served from our service in the cloud, or ask us to do so for you). We regard a problem as a form of valuable content, but our commitment and vision is also to promote the sharing of problems and the collaborative design of didactical paths and experiences articulated in interactive problems. A well-designed problem, like a Montessori game, can teach better than a perfect essay on a subject.

make localtest: prepares all files required to test a solution model in local. Once this generation is complete, it also executes the evaluation of a default solution model.

make core: prepares all files required to test in local any solution model of your choice.

make inputs: will generate the testcases (input_*.dat and input_*.txt) files for the inputs folder. This folder contains the testcases for testing the solutions submitted to the online evalution service.

make clean-inputs: deletes the folder inputs.

make pdf: generates the pdf files with the statement of the problem or other presentation material.

make clean: deletes all the automatically generated files or other temporary files.
