#!/bin/bash
problem_name=$(basename ${PWD##*.})
prefix_generator=./instance-generators/generator_${problem_name}
prefix_converter=./instance-generators/converter_${problem_name}_dat2txt

if [ -e ${prefix_generator}_txt.cpp ]; then
    if [ ! -x ${prefix_generator}_txt.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_generator}_txt.bin ${prefix_generator}_txt.cpp
    fi 
fi 
if [ -x ${prefix_generator}_txt.bin ]; then
    ${prefix_generator}_txt.bin $@
    exit 0
fi 
if [ -x ${prefix_generator}_txt.py ]; then
    ${prefix_generator}_txt.py $@
    exit 0
fi 
if [ -e ${prefix_generator}_dat.cpp ]; then
    if [ ! -x ${prefix_generator}_dat.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_generator}_dat.bin ${prefix_generator}_dat.cpp
    fi 
fi 
if [ -e ${prefix_converter}.cpp ]; then
    if [ ! -x ${prefix_converter}.bin ]; then
        g++ -Wall --pedantic -O2 -o ${prefix_converter}.bin ${prefix_converter}.cpp
    fi 
fi
generator=""
converter=""
if [ -x ${prefix_generator}_dat.bin ]; then
    generator=${prefix_generator}_dat.bin
fi 
if [ -x ${prefix_generator}_dat.py ]; then
    generator=${prefix_generator}_dat.py
fi 
if [ -x ${prefix_converter}.bin ]; then
    converter=${prefix_converter}.bin
fi 
if [ -x ${prefix_converter}.py ]; then
    converter=${prefix_converter}.py
fi 
if [ -x ${generator} ] && [ -x ${converter} ]; then
    ${generator} $@ | ${converter}
    exit 0
fi

(>&2 echo "Sorry: No generator path available at present. If the generators are provided check that their execute permission are granted." )
exit 1
