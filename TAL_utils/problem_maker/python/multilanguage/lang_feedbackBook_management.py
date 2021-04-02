#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv

import ruamel
from termcolor import colored, cprint

usage = f"""\nLaunch as:\n
> {argv[0]} service_server.py\n
and this utility will extract and cat to stdout the workbook of pharases hardcoded in the file with name "service_server.py". This name can be a fullname (i.e., include a path to locate the resource) and the file is assumed to be a service server implementetion for a TALight problem. Currently this utility is guaranteed to work for servers written in python whose mutilanguage support rests on the multilanguage.py module of the TALight library in support to the problem maker. But we expect/aim this utility should also work (or be readily adapted) also for other languages for which the Lang class offered by the multilanguage.py module has been translated or implemented without introducing differences in the interface for using its basic functionalities. Whether and how the utils should be split by language is a question that will be more clearly/properly addressed only in the future, whence it is best to keep things under a same hood for now."""

if len(argv) != 2:
    for out in {stdout, stderr}:
        print("Wrong call to the TAL_util {argv[0]}.\n see what gone on stdout to know more", file=out)
    print(usage)
    exit(1)
try:
    service_server_program_file = open(argv[1], 'r')
    program_lines = service_server_program_file.readlines()
except IOError as ioe:
    for out in {stdout, stderr}:
        print(f'Problem detected: file "{argv[1]}" could not be accessed.', file=out)
        print(' This operation is necessary given what you have required to do. Util aborted.', file=out)
        print(ioe, file=out)
    exit(1)


collection_of_hardcoded = "None"
list_of_hardcoded = "None"

collection_in_yaml_book = "None"
list_in_yaml_book = "None"

filename_yaml_book = "None"
filename_server_code = "None"
filename_server_lang = "python"


def LANG_render_feedback(fstring):
    return eval(f"f'{fstring}'")

def print_out_all_phrases_in_list(list_of_phrases):
    for phrase in list_of_phrases:
        code, content_verbatim = phrase
        print(code + ":", end= " ")
        print(content_verbatim)

def print_out_one_phrase_in_all_collections(phrase_code, collections_list):
    if len(collections_list) == 1:
        cprint(phrase_code + ":", "yellow", ["bold"], end= " ")
    else:
        cprint(phrase_code + ":", "yellow", ["bold"]) 
        
    for collection_source, collection_of_phrases in collections_list:
      if phrase_code not in collection_of_phrases:
        cprint(colored("missing in source: ", "red"), collection_source)   
      else:
        print(collection_of_phrases[phrase_code])

try:
  with open(meta_yaml_file, 'r') as stream:
    try:
        meta_yaml_book = ruamel.yaml.safe_load(stream)
    except:
        print(f'Problem detected: The meta.yaml file "{messages_book_file}" could not be loaded as a .yaml file.')
        print(' This operation is necessary given what you have required to do. Util aborted.')
        exit(1)
except IOError as ioe:
    print(f'Problem detected: The meta.yaml file {meta_yaml_file} could not be accessed for the required information.')
        print(' This operation is necessary given what you have required to do. Util aborted.')
        print(ioe, file=out)
    exit(1)

if ENV['service'] not in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("wrong-service-name", f'\nSorry, you asked information about {ENV["service"]} which however does not appear among the services currently supported for the problem {problem}.'), "red", ["bold"])
    TAc.print("\n\nList of all Services:", "red", ["bold", "underline"], end="  ")
    print(", ".join(meta_yaml_book['services'].keys()),end="\n\n")
    exit(0)

TAc.print("\n"+ENV['service'], "yellow", ["bold"], end="")
TAc.print(LANG.render_feedback("service-of", f'   (service of the {problem} problem)'), "yellow")

if "explain" in meta_yaml_book['services'][ENV['service']].keys():
    TAc.print("\nDescription:", "green", ["bold"])
    print("   "+eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['explain'])}'"))
if len(meta_yaml_book['services'][ENV['service']]['args']) > 0:
    TAc.print(LANG.render_feedback("the-num-arguments", f'\nThe {len(meta_yaml_book["services"][ENV["service"]]["args"])} arguments of service {ENV["service"]}:'), "green", ["bold"])
    for a,i in zip(meta_yaml_book['services'][ENV['service']]['args'],range(1,1+len(meta_yaml_book['services'][ENV['service']]['args']))):
        TAc.print(str(i)+". ", "white", ["bold"], end="")
        TAc.print(a, "yellow", ["bold"])
        TAc.print("   regex: ", ["bold"], end="")
        print(meta_yaml_book['services'][ENV['service']]['args'][a]['regex'])
        if "explain" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Explanation: ", ["bold"], end="")
            print(eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['args'][a]['explain'])}'"))
        if "example" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Example: ", ["bold"], end="")
            print(eval(f"f'{str(meta_yaml_book['services'][ENV['service']]['args'][a]['example'])}'"))
        if "default" in meta_yaml_book['services'][ENV['service']]['args'][a].keys():
            TAc.print("   Default Value: ", ["bold"], end="")
            print(str(meta_yaml_book['services'][ENV['service']]['args'][a]['default']))
        else:
            TAc.print(f"   The argument {a} is mandatory.", ["bold"])

print(LANG.render_feedback("regex-cloud-resource", f"\nAll arguments of all TALight services take in only strings as possible values. As you can see, the family of string values allowed for an argument is described by means of a regex. We refer to the online service 'https://extendsclass.com/regex-tester.html' if in need of help in grasping the intended meaning of the regex.\n"))

# Now printing the footing lines:
if "help" in meta_yaml_book['services'].keys():
    TAc.print(LANG.render_feedback("index-help-pages", 'Index of the Help Pages:'), "red", ["bold", "underline"], end="  ")
    print(meta_yaml_book['services']['help']['args']['page']['regex'][2:-2])
TAc.print(LANG.render_feedback("list-services", 'List of all Services:'), "red", ["bold", "underline"], end="  ")
print(", ".join(meta_yaml_book['services'].keys()))

    
exit(0)




