#!/bin/bash
problem_name=$(basename $(dirname ${PWD##*.}))
if [[ $# -le 0 ]] ; then
    model_file=${problem_name}_always_answer_42.mod
else
   model_file=$1
fi

cat $model_file | sed -e '/^\*/d' -e '/^\//d' -e 's/ > "output.txt"//g' -e 's/> "output.txt"//g' -e 's/>"output.txt"//g' > to_be_submitted.mod
cat ../examples/input_1.dat >> to_be_submitted.mod 

echo "The model+data file to be submitted for format and syntax verification:"
echo "   to_be_submitted.mod"
echo "has been generated from the template model_file:"
echo "   $model_file"
echo "and the data file"
echo "   ../examples/input_1.dat"
echo
echo "To check compliance with AMPL use a local installation or the free online service:"
echo "  https://ampl.com/cgi-bin/ampl/amplcgi"
echo 'fill-in only the "Model and data" input-box with the content of the generated to_be_submitted.mod file.'
echo "To check compliance with GMPL use the free and readily set-up local installation."
