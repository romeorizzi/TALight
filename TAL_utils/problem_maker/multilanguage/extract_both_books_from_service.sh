#!/bin/bash
if [ -f $1_feedbackBook.en.yaml ]; then
    echo "WARNING: $1_feedbackBook.en.yaml  already exists."
    echo "Please, remove it if you really want me to create one."
else
    ~/TALight/TAL_utils/problem_maker/python/multilanguage/extract_feedbackBook_hardcoded.py $1_server.py fstring_count -preamble_file=/home/romeo/TALight/TAL_utils/problem_maker/python/multilanguage/preamble.en.yaml 1> $1_feedbackBook.en.yaml 
fi
echo
if [ -f $1_feedbackBook.it.yaml ]; then
    echo "WARNING: $1_feedbackBook.it.yaml  already exists."
    echo "Please, remove it if you really want me to create one."
else
    ~/TALight/TAL_utils/problem_maker/python/multilanguage/extract_feedbackBook_hardcoded.py $1_server.py fstring_count -preamble_file=/home/romeo/TALight/TAL_utils/problem_maker/python/multilanguage/preamble.it.yaml 1> $1_feedbackBook.it.yaml
fi
