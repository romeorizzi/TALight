#!/bin/bash
problem_name=$(basename ${PWD##*.})
prefix_solver=./reference-outputs-generators/solver_${problem_name}
prefix_converter=./instance-generators/converter_${problem_name}
fastest_model=./models/${problem_name}_fastest-model.mod

if [ -e ${prefix_solver}_txt2txt.cpp ]; then
    if [ ! -x ${prefix_solver}_txt2txt.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_solver}_txt2txt.bin ${prefix_solver}_txt2txt.cpp
    fi 
fi 
if [ -x ${prefix_solver}_txt2txt.bin ]; then
    ${prefix_solver}_txt2txt.bin < $@
    exit 0
fi 
if [ -x ${prefix_solver}_txt2txt.py ]; then
    ${prefix_solver}_txt2txt.py < $@
    exit 0
fi
if [ -e ${prefix_converter}_txt2dat.cpp ]; then
    if [ ! -x ${prefix_converter}_txt2dat.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_converter}_txt2dat.bin ${prefix_converter}_txt2dat.cpp
    fi 
fi 
if [ -e ${prefix_solver}_dat2txt.cpp ]; then
    if [ ! -x ${prefix_solver}_dat2txt.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_solver}_dat2txt.bin ${prefix_solver}_dat2txt.cpp
    fi 
fi 
converter=""
solver=""
if [ -x ${prefix_converter}_txt2dat.bin ]; then
    converter=${prefix_converter}_txt2dat.bin
fi 
if [ -x ${prefix_converter}_txt2dat.py ]; then
    converter=${prefix_converter}_txt2dat.py
fi 
if [ -x ${prefix_solver}_dat2txt.bin ]; then
    solver=${prefix_solver}_dat2txt.bin
fi 
if [ -x ${prefix_solver}_dat2txt.py ]; then
    solver=${prefix_solver}_dat2txt.py
fi 
if [ ! -z ${converter} ] && [ ! -z  ${solver} ]; then
    ${converter} < $@ | ${solver}
    exit 0
fi

(>&2 echo "Warning: No solver path in standard languages (like cpp or python) available at present. If such solvers are provided check that their execute permission is granted.\nThese solvers are preferred because they could provide very quickly (in secs) solutions to large instances (taking houers to be solved through a model).\nNow we try using a GMPL model you might have choosen as your reference, linking to it from the symbolic link $fastest_model we use here below (and elsewhere needed).")

if [ -x ${converter} ] && [ -e ${fastest_model} ]; then
    ${converter} < $@ > tmp_input.dat
    glpsol -m ${fastest_model} -d tmp_input.dat > /dev/null
    cat output.txt
    rm -f output.txt tmp_input.dat
    exit 0
fi 

(>&2 echo "Error: No solver path whatsoever appears available at present. If such solvers are provided check that their execute permission is granted.\nWhen possible (usually for problems in P), the preference is for solvers in standard languages (like cpp or python) since they can very quickly answer also on heavy instances, and also offer an independent check.\n")

exit 1
