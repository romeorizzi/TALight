#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="morra"
service="compute_hash"
args_list = [
    ('hash_type',str),
    ('white_string',str),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import stderr, exit, argv
import string 
import random

from hash_and_cipher import hash_value

from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
        

if ENV['white_string'] not in {None, "None"}:
    TAc.print(f"{hash_value(ENV['white_string'],ENV['hash_type'])}", "yellow")
else:
    TAc.print(LANG.opening_msg, "green")
    TAc.print(LANG.render_feedback("ask-for-white-string", "Since the parameter white_string was not specified in this call, we now ask you to insert the string in white, of which to compute the hash:"), "yellow", ["bold"])
    white_str=input()
    TAc.print(f"h({white_str}) = {hash_value(white_str,ENV['hash_type'])}", "yellow")
    
exit(0)
