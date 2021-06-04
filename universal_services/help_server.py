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

ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), book_strictly_required=True)
TAc.print(LANG.opening_msg, "green")

page = LANG.messages_book[ENV["page"]]
for line in page:
    if type(line)==str:
        print(line, end="")
    elif len(line)==2:
        TAc.print(line[0], line[1], end="")        
    elif len(line)==3:
        TAc.print(line[0], line[1], line[2], end="")        
exit(0)
