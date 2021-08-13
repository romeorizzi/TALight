#!/bin/zsh

PATH_TO_EXE=$HOME/github/TALight/TAL_utils/problem_maker/python/multilanguage
PATH_TO_PREAMBLE=$HOME/github/TALight/TAL_utils/problem_maker/python/multilanguage


# REMOVE BOOKS
if [ "$1" = "clean" ]; then
    rm *en.yaml
    # rm utils_lang_feedbackBook.en.yaml 
fi


# CREATE BOOKS
if [ "$1" = "en" ]; then
    # get _server.py files
    files=(`find . -type f -iname "*_server.py"`)
    for entry in $files
    do
        file="${entry:2:-10}"
        echo $file
        if [ -f ${file}_feedbackBook.en.yaml ]; then
            echo "WARNING: ${file}_feedbackBook.en.yaml  already exists."
        else
            $PATH_TO_EXE/extract_feedbackBook_hardcoded.py ${file}_server.py fstring_count -preamble_file=$PATH_TO_PREAMBLE/preamble.en.yaml 1> ${file}_feedbackBook.en.yaml 
        fi
    done
    # get extra files
    file="utils_lang"
    echo $file
    $PATH_TO_EXE/extract_feedbackBook_hardcoded.py ${file}.py fstring_count -preamble_file=$PATH_TO_PREAMBLE/preamble.en.yaml 1> ${file}_feedbackBook.en.yaml 
fi


if [ "$1" = "it" ]; then
    # get _server.py files
    files=(`find . -type f -iname "*_server.py"`)
    for entry in $files
    do
        file="${entry:2:-10}"
        echo $file
        if [ -f ${file}_feedbackBook.en.yaml ]; then
            echo "WARNING: ${file}_feedbackBook.it.yaml  already exists."
        else
            $PATH_TO_EXE/extract_feedbackBook_hardcoded.py ${file}_server.py fstring_count -preamble_file=$PATH_TO_PREAMBLE/preamble.it.yaml 1> ${file}_feedbackBook.it.yaml 
        fi
    done
    # get extra files
    file="utils_lang"
    echo $file
    $PATH_TO_EXE/extract_feedbackBook_hardcoded.py ${file}.py fstring_count -preamble_file=$PATH_TO_PREAMBLE/preamble.it.yaml 1> ${file}_feedbackBook.it.yaml 
fi