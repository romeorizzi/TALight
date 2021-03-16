#!/usr/bin/env python3
from sys import stderr, exit, argv
from os import environ

from multilanguage import Env, Lang, TALcolors

problem=environ["TAL_META_DIR"].split("/")[-1]
service="help"
args_list = [
    ('page',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), book_required=True)
TAc.print(LANG.opening_msg, "green")

# BEGIN: print the help page

page = LANG.messages_book[ENV["page"]]
for line in page:
    if type(line)==str:
        print(line, end="")
    elif len(line)==2:
        TAc.print(line[0], line[1], end="")        
    elif len(line)==3:
        TAc.print(line[0], line[1], line[2], end="")

# END: print the help page

# Now printing the footing lines:

import ruamel
meta_yaml_file = environ['TAL_META_DIR'] + "/meta.yaml"
try:
  with open(meta_yaml_file, 'r') as stream:
    try:
        meta_yaml_book = ruamel.yaml.safe_load(stream)
    except:
        exit(0)
    TAc.print(LANG.messages_book['services-list'], "red", ["bold", "underline"], end="  ")
    print(", ".join(meta_yaml_book['services'].keys()))
    TAc.print(LANG.messages_book['help-pages'], "red", ["bold", "underline"], end="  ")
    print(meta_yaml_book['services']['help']['args']['page']['regex'][2:-2])
except:
    #print(f"meta_yaml_file={meta_yaml_file}")
    exit(0)

    
exit(0)
