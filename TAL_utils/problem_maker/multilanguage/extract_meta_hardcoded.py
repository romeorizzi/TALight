#!/usr/bin/env python3
from sys import stderr, stdout, exit, argv
import os
import ruamel.yaml

usage=f"""
This util extracts the descriptional information contained in the meta.yaml file of a problem and creates the single service files contained in the lang/hardcoded_ext/meta/ subfolder of the problem folder.
These smaller files can be accessed more convenienly but also offer a convenient basis and reference for their translation to other languages.
 
Usage: argv[0] [ fullname_problem_folder [ service ]  ]

When no argument is given then it is assumed that the problem folder is the current one and that the action is required for each one of the services of that problem.

One single argument is interpreted as the fullpath to a problem folder and, again, action is taken for all of its services.

Example 1 of use:
    argv[0]

What will happen here:
    if you are in the main folder of a problem (the one containing its meta.yaml file) then the utility will yield the files in ./lang/hardcoded_ext/meta/  for each one of its services. 

Example 2 of use:
    argv[0] ~/TALight/example_problems/tutorial/pills
or
    argv[0] ../pills

What will happen here:
    Since the folder pills contains its meta.yaml file (indeed, pills is one of the problems in our tutorial) then the utility yields the files in .../pills/lang/hardcoded_ext/meta/  for each one of the services of problem pills.

Example 3 of use:
     argv[0] ~/TALight/example_problems/tutorial/pills/pills check_num_sol
or
     argv[0] . pills check_num_sol

What will happen here:
    The utility yields the file in .../pills/lang/hardcoded_ext/meta/  only for the service check_num_sol of problem pills.
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


def yield_one_service(problem_folder, service_name):
    print(f"service_name={service_name}", end="")
    meta_yaml_file = os.path.join(problem_folder, 'meta.yaml')
    meta_yaml = open(meta_yaml_file, 'r')
    service_meta_yaml_file = os.path.join(problem_folder, 'lang', 'hardcoded_ext', 'meta', f'meta_{service_name}_hardcoded_ext.yaml')
    if os.path.exists(service_meta_yaml_file):
        print(f"{CRED}WARNING:{CEND} mi chiedi di creare un file che già è presente:\n    {service_meta_yaml_file}\n")
        answ = input("Immetti 'p' o 'P' per proseguire sovrascivendo il vecchio file,  'k' o 'K'  per skippare su questo servizio del problema e passare ai successivi. Con ogni altra immissione esci: ").upper()
        if answ == 'K':
            return
        if answ != 'P': 
            exit(1)
    service_meta_yaml = open(service_meta_yaml_file, 'w')
    section_services_begun = False
    inside_my_service = False
    left_margin_width = 0
    for line in meta_yaml.readlines():
        if not section_services_begun:
            print(line, file=service_meta_yaml, end="")
            if line[:9] == "services:":
                section_services_begun = True
        else:
            if left_margin_width == 0:
                without_margin = line.lstrip()
                if len(without_margin) == 0  or  without_margin[0] == "#":
                    continue
                left_margin_width = len(line) - len(without_margin)
            if line[:left_margin_width] == " "*(left_margin_width):
                if line[left_margin_width] not in {" ","#"}:
                    print(line, file=service_meta_yaml, end="")
                    if service_name in line:
                        inside_my_service = True
                    else:
                        inside_my_service = False
                elif inside_my_service:
                    print(line, file=service_meta_yaml, end="")
    print('...', file=service_meta_yaml)
    print(f"  {CBOLD}{CGREEN}Ok{CEND}")


if len(argv) > 3:
    print(usage)
    exit(0)

if len(argv) == 1:
    problem_folder = os.getcwd()
else:
    problem_folder = argv[1]
if problem_folder[-1] in {'/','\\'}:
    problem_folder = problem_folder[:-1]
problem_name=problem_folder.split('/')[-1]
print(f"problem_name={problem_name}    problem_folder={problem_folder}")

meta_yaml_file = os.path.join(problem_folder, 'meta.yaml')
try:
  with open(meta_yaml_file, 'r') as stream:
    try:
        meta_yaml_book = ruamel.yaml.safe_load(stream)
    except:
        for out in [stdout, stderr]:
            print(f'{CBOLD}{CRED}Error:{CEND} The meta.yaml file \'\'{meta_yaml_file}\'\' could not be loaded as a .yaml file.', file=out)
        exit(0)    
except IOError as ioe:
    for out in [stdout, stderr]:
        print(f'{CBOLD}{CRED}Error:{CEND} No meta.yaml file has been found in the problem folder \'\'{problem_folder}\'\'.\nFile not found:\n     \'\'{meta_yaml_file}\'\'.', file=out)
        print(ioe, file=out)
        exit(0)

if len(argv) == 3:
    if argv[2] not in meta_yaml_book['services'].keys():
        for out in [stdout, stderr]:
            print(f'{CBOLD}{CRED}Error:{CEND} The meta.yaml file \'\'{meta_yaml_file}\'\' does not include a service of name:\n    {argv[2]}', file=out)
        exit(0)    
    yield_one_service(problem_folder, service_name=argv[2])
else:
    for service in meta_yaml_book['services'].keys():
        yield_one_service(problem_folder, service_name=service)

exit(0)



