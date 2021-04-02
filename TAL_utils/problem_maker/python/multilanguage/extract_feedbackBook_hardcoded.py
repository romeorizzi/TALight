#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
import re
import ruamel

usage = f"""\nUsage:\nLaunch as:\n
> {argv[0]} service_server.py ["only_fstring_phrases"|"only_plain_phrases"|"fstring_signal"|"fstring_count"] [-preamble_file=<premble_file_name>]\n
and this utility will extract and cat to stdout the workbook of pharases hardcoded in the file with name "service_server.py". This name can be a fullname (i.e., include a path to locate the resource) and the file is assumed to be a service server implementetion for a TALight problem.

The second argument is optional and takes up one of the following values:
"only_fstring_phrases" --> cats to stdout only those phrases that undergo fstring interpretation
"only_plain_phrases" --> cats to stdout only those phrases that do NOT undergo fstring interpretation
"fstring_signal" --> cats to stdout all phrases (like in standard usage, when no optional parameter is provided) but those that undergo fstring interpretation are clarly marked (WARNING: this means that the feedbackBook cat to stdout is NOT a valid feedbackBook)
"fstring_count" --> cats to stdout all phrases (like in standard usage, when no optional parameter is provided) but it also prints on stderr the stats about those phrases that undergo fstring interpretation (NOTE: this means that the feedbackBook cat to stdout is a valid feedbackBook and you CAN use it by redirecting only stdout to a file (pipe with " 1>" rather than with just " >")).

The third argument is optional and should begin with "-preamble_file=" followed by the name of a correct preamble file for the intended language (see for example the files preamble.en.yaml and preamble.it.yaml contained in the folder of this script). When this argument is provided that preamble file is prepended in order to obtain a complete feedbackBook for that language (of course, the sentences following the preamble will still need to get translated from the hardcoded language, which we suggest should be English to facilitate translating in any other language. The other languages will need to use other characters. On one side this is greatly simplified since .yaml files are UTF-8. Still it could be a problem to have to use some characters like unpairs ' and ". The rules to follow to deal with these with no trouble are here more below.

This utility is guaranteed to work for servers written in python whose mutilanguage support rests on the multilanguage.py module of the TALight library in support to the problem maker. The utility also works for (or can be readily adapted (and possibly also translated into) other languages for which the Lang class offered by the multilanguage.py module has been translated or implemented.
In his *_server.py files one should also adhere to:
1. use single quotes ' to embrace the whole message string
2. always alternate between ' and " when nesting them
3. when you need to use an unpaired ' write \\'' i.e. a backslash followed by two '
4. when you need to use an unpaired " write \\"" i.e. a backslash followed by two "
"""

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
            print("Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
        print(f"Your optional argument ({fstring_arg}) in not among those allowed")
        print(usage)
        exit(1)
if len(argv) in {4}:
    string_arg3 = argv[3]
    if not string_arg3[0:15] == '-preamble_file=':
        for out in {stdout, stderr}:
            print("Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
        print(f"Your third optional argument ({string_arg3}) in not among those allowed")
        print(usage)
        exit(1)
    premble_file_name=string_arg3[15:]
    try:
        premble_file = open(premble_file_name, 'r')
        preamble = premble_file.read()
    except IOError as ioe:
        for out in {stdout, stderr}:
            print(f'Problem detected: file "{premble_file_name}" could not be accessed.', file=out)
            print(' This operation is necessary given what you have required to do. Util aborted.', file=out)
        print(ioe, file=stderr)
        exit(1)

try:
    service_server_program_file = open(argv[1], 'r')
    program_lines = service_server_program_file.readlines()
except IOError as ioe:
    for out in {stdout, stderr}:
        print(f'Problem detected: file "{argv[1]}" could not be accessed.', file=out)
        print(' This operation is necessary given what you have required to do. Util aborted.', file=out)
    print(ioe, file=stderr)
    exit(1)

if len(argv) > 3:
    print(preamble)

program_source = f"ORIGINAL CONTENT OF FILE {argv[1]}" + "".join(program_lines)
#print(program_source)

# We should search and treat patterns like:
#   LANG.render_feedback("insert-num-rows", 'Insert the number of rows:')

def extract_phrase(good_suffix):
    interesting_part = ""
    balance = 0
    for char in good_suffix:
        interesting_part += char 
        if char == '(':
            balance += 1
        if char == ')':
            balance -= 1
            if balance == 0:
                break
    #print(interesting_part)
    while interesting_part[-1] not in {"'",'"'}:
        interesting_part = interesting_part[0:-1]
    interesting_part = interesting_part[0:-1]
    #print(re.split('(\"|\')', interesting_part, 3))
    _,_,phrase_code,_,fstring_flag,_,phrase_text = re.split('(\"|\')', interesting_part, 3)
    return phrase_code, phrase_text, "f" in fstring_flag


found_phrases = {}

source_good_suffix = program_source
num_plain_phrases = 0
num_fstring_phrases = 0
while re.search("LANG.render_feedback", source_good_suffix, 1) != None:
    gone_away_part, source_good_suffix = re.split("LANG.render_feedback", source_good_suffix, 1)
    phrase_code, phrase_text,fstring_flag = extract_phrase(source_good_suffix)
    if phrase_code in found_phrases.keys():
        if phrase_text == found_phrases[phrase_code]:
            continue
        else:
            print(f"\nERROR:\n duplicated code: {phrase_code}\n sentence in first occurrence: {found_phrases[phrase_code]}\n different sentence in later occurrences: {phrase_text}\n",file=stderr)            
    if fstring_flag:
        num_fstring_phrases +=1
    else:
        num_plain_phrases += 1
    if fstring_arg in {None, "fstring_count"}:
        print(f"{phrase_code}: '{phrase_text}'")
    elif fstring_arg == "only_fstring_phrases" and fstring_flag:
        print(f"{phrase_code}: '{phrase_text}'")
    elif fstring_arg == "only_plain_phrases" and not fstring_flag:
        print(f"{phrase_code}: '{phrase_text}'")
    elif fstring_arg in {"fstring_signal"}:
        if fstring_flag:
            print(f"{phrase_code}: [THIS IS AN FSTRING] '{phrase_text}'")
        else:
            print(f"{phrase_code}: '{phrase_text}'")

if fstring_arg == "fstring_count":
    print(f"\nSUMMARY:\n num_phrases (TOTAL): {num_plain_phrases+num_fstring_phrases}\n num_plain_phrases: {num_plain_phrases}\n num_fstring_phrases: {num_fstring_phrases}\n",file=stderr)
        
exit(0)




