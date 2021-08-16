#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
import re
import ruamel
import ast

usage = f"""\nUsage:\nLaunch as:\n
> {argv[0]} service_server.py ["only_fstring_phrases"|"only_plain_phrases"|"fstring_signal"|"fstring_count"] [-preamble_file=<premble_file_name>]\n
and this utility will extract and cat to stdout the workbook of pharases hardcoded in the file with name "service_server.py". This name can be a fullname (i.e., include a path to locate the resource) and the file is assumed to be a service server implementetion for a TALight problem.

The second argument is optional and takes up one of the following values:
"only_fstring_phrases" --> cats to stdout only those phrases that undergo fstring interpretation
"only_plain_phrases" --> cats to stdout only those phrases that do NOT undergo fstring interpretation
"fstring_signal" --> cats to stdout all phrases (like in standard usage, when no optional parameter is provided) but those that undergo fstring interpretation are clarly marked (WARNING: this means that the feedbackBook cat to stdout is NOT a valid feedbackBook)
"fstring_count" --> cats to stdout all phrases (like in standard usage, when no optional parameter is provided) but it also prints on stderr the stats about those phrases that undergo fstring interpretation (NOTE: this means that the feedbackBook cat to stdout is a valid feedbackBook and you CAN use it by redirecting only stdout to a file).

The third argument is optional and should begin with "-preamble_file=" followed by the name of a correct preamble file for the intended language (see for example the files preamble.en.yaml and preamble.it.yaml contained in the folder of this script). When this argument is provided that preamble file is prepended in order to obtain a complete feedbackBook for that language (of course, the sentences following the preamble will still need to get translated from the hardcoded language, which we suggest should be English to facilitate translating in any other language. The other languages will need to use other characters. On one side this is greatly simplified since .yaml files are UTF-8. Still it could be a problem to have to use some characters like  ' and ". The rules to follow to deal with these with no trouble are collected and reported here more below.

This utility is guaranteed to work for servers written in python whose mutilanguage support rests on the multilanguage.py module of the TALight library in support to the problem maker. The utility also works for (or can be readily adapted (and possibly also translated into) other languages for which the Lang class offered by the multilanguage.py module has been translated or implemented.
In his *_server.py files one should also adhere to:
1. use single quotes ' to embrace the whole message string
2. always alternate between ' and " when nesting them
3. when you need to use an unpaired ' then in the feedbackBook yaml file write \\'' i.e. a backslash followed by two ', whereas in the code whas written \\'\\'
4. when you need to use an unpaired " then in the feedbackBook yaml file write \\"" i.e. a backslash followed by two ", whereas in the code whas written \\"\\"
5. for simplicity, consider using ` more frequently instead
"""


CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'


def adapt_string_to_yaml_book(string):
    #print("before: " + string, file=stderr)
    orderd_list_of_substitutions = [("\\'","\\''"),  # substitutes an \' placed in the code with an \'' placed in the wordbook yaml. file
                                    ('\\"','\\""'),  # substitutes an \" placed in the code with an \"" placed in the wordbook yaml. file
                                   ]
    for before,after in orderd_list_of_substitutions:
       string = string.replace(before, after)
    #print("after: " + string, file=stderr)
    return(string)


def is_valid_python(code):
   try:
       ast.parse(code)
   except SyntaxError:
       return False
   return True

def the_longest_valid_python_string_which_is_prefix_of(blob):
   first_char = blob[0]
   mate_of = { "(":")", "'":"'", '"':'"' }
   assert first_char in mate_of.keys()
   expected_last_char = mate_of[first_char]
   j = len(blob) -1
   while True:
       while blob[j] != expected_last_char:
           j -= 1
       assert j > 0
       if is_valid_python(blob[:j+1]):
           return blob[:j+1]
       j -= 1

fstring_arg = None
if len(argv) not in {2,3,4}:
    for out in {stdout, stderr}:
        print("Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
    print(usage)
    exit(1)
if len(argv) in {3,4}:
    fstring_arg = argv[2]
    if not fstring_arg in {None, "only_fstring_phrases", "only_plain_phrases","fstring_signal","fstring_count"}:
        for out in {stdout, stderr}:
            print(f"{CBOLD}{CRED}Error:{CEND} Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
        print(f"Your optional argument ({fstring_arg}) in not among those allowed")
        print(usage)
        exit(1)
if len(argv) in {4}:
    string_arg3 = argv[3]
    if not string_arg3[0:15] == '-preamble_file=':
        for out in {stdout, stderr}:
            print(f"{CBOLD}{CRED}Error:{CEND} Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
        print(f"Your third optional argument ({string_arg3}) in not among those allowed")
        print(usage)
        exit(1)
    premble_file_name=string_arg3[15:]
    try:
        premble_file = open(premble_file_name, 'r')
        preamble = premble_file.read()
    except IOError as ioe:
        for out in {stdout, stderr}:
            print(f'{CBOLD}{CRED}Problem detected:{CEND} file "{premble_file_name}" could not be accessed.', file=out)
            print(' This operation is necessary given what you have required to do. Util aborted.', file=out)
        print(ioe, file=stderr)
        exit(1)

try:
    service_server_program_file = open(argv[1], 'r')
    program_lines = service_server_program_file.readlines()
except IOError as ioe:
    for out in {stdout, stderr}:
        print(f'{CBOLD}{CRED}Problem detected:{CEND} file "{argv[1]}" could not be accessed.', file=out)
        print(' This operation is necessary given what you have required to do. Util aborted.', file=out)
    print(ioe, file=stderr)
    exit(1)

if len(argv) > 3:
    print(preamble)

program_source = f"ORIGINAL CONTENT OF FILE {argv[1]}" + "".join(program_lines)
#print(program_source)

# We should search and treat patterns like:
#   LANG.render_feedback("insert-num-rows", 'Insert the number of rows:')
#                           ^ phrase_code       ^ phrase_text
def extract_phrase(good_prefix):
    assert good_prefix[0] == '(' # which is the open parentheses of the next LANG.render_feedback(...  call
#                                                                                                ^ more precisely, this one
    embraced_call = the_longest_valid_python_string_which_is_prefix_of(good_prefix)
    #print(f"good_prefix={good_prefix}")
    #print(f"embraced_call={embraced_call}")
    start_pos_phrase_code = 1
    while embraced_call[start_pos_phrase_code] not in { "'", '"' }:
        start_pos_phrase_code += 1
    delimiter = embraced_call[start_pos_phrase_code]
    stop_pos_phrase_code = start_pos_phrase_code + 1
    while embraced_call[stop_pos_phrase_code] != delimiter:
        stop_pos_phrase_code += 1
    phrase_code = embraced_call[start_pos_phrase_code+1:stop_pos_phrase_code]
    #print(f"phrase_code={phrase_code}")
    start_pos_hardcoded_phrase = stop_pos_phrase_code + 1
    while embraced_call[start_pos_hardcoded_phrase] not in { "'", '"' }:
        start_pos_hardcoded_phrase += 1
    phrase_text = the_longest_valid_python_string_which_is_prefix_of(embraced_call[start_pos_hardcoded_phrase:])[1:-1]
    #print(f"phrase_text={phrase_text}")
    return phrase_code, phrase_text, "f" in embraced_call[stop_pos_phrase_code:start_pos_hardcoded_phrase]


found_phrases = {}

num_plain_phrases = 0
num_fstring_phrases = 0
segments=program_source.split("LANG.render_feedback")[1:]
for segment_starting_with_LANG_call_open_par in segments:
    phrase_code, phrase_text,fstring_flag = extract_phrase(segment_starting_with_LANG_call_open_par)
    if phrase_code in found_phrases.keys():
        if phrase_text == found_phrases[phrase_code]:
            continue
        else:
            print(f"\n{CBOLD}{CRED}WARNING:\n duplicated code:{CEND} {phrase_code}\n -message sentence in first occurrence:\n--->{found_phrases[phrase_code]}\n -different message sentence in later occurrences:\n--->{phrase_text}\n{CBOLD}{CRED}NOTICE:{CEND} we deal with this issue by discarding the later occurrences and keeping only the very first one encountered (which might had been the one commented out).",file=stderr)
    else:
        found_phrases[phrase_code] = phrase_text
    if fstring_flag:
        num_fstring_phrases +=1
    else:
        num_plain_phrases += 1
        
    if fstring_arg in {None, "fstring_count"}:
        print(f"{phrase_code}: '{adapt_string_to_yaml_book(phrase_text)}'")
    elif fstring_arg == "only_fstring_phrases" and fstring_flag:
        print(f"{phrase_code}: '{adapt_string_to_yaml_book(phrase_text)}'")
    elif fstring_arg == "only_plain_phrases" and not fstring_flag:
        print(f"{phrase_code}: '{adapt_string_to_yaml_book(phrase_text)}'")
    elif fstring_arg in {"fstring_signal"}:
        if fstring_flag:
            print(f"{phrase_code}: [THIS IS AN FSTRING] '{adapt_string_to_yaml_book(phrase_text)}'")
        else:
            print(f"{phrase_code}: '{adapt_string_to_yaml_book(phrase_text)}'")

if fstring_arg == "fstring_count":
    print(f"\n{CBOLD}{CGREEN}SUMMARY:{CEND}\n num_phrases (TOTAL): {num_plain_phrases+num_fstring_phrases}\n num_plain_phrases: {num_plain_phrases}\n num_fstring_phrases: {num_fstring_phrases}\n",file=stderr)
        
exit(0)




