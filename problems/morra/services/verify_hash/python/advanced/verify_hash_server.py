#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="morra"
service="verify_hash_server"
args_list = [
    ('num_checks',int),
    ('hash_type',str),
    ('alphabet_white_string',str),
    ('length_white_string',int),
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
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:


for i in range(1,ENV['num_checks']+1):
    if ENV['alphabet_white_string'] == "safely_printable":
        alphabet_string = string.ascii_letters + string.digits + string.punctuation
    else:
        alphabet_string = getattr(string, ENV['alphabet_white_string'])
    white_string = ''.join(random.choices(alphabet_string, k=ENV['length_white_string']))
    TAc.print(LANG.render_feedback("prompt", "Please, compute and send me the hash of the following string:"), "yellow")
    TAc.print(f"{white_string}", "yellow", ["bold"])
    hash_str_submitted=input()
    hash_str_true=hash_value(white_string,ENV['hash_type'])
    if hash_str_submitted==hash_str_true:
        TAc.OK()
        TAc.print(LANG.render_feedback("give-hash-verbose", f"indeed, h({white_string}) = {hash_value(white_string,ENV['hash_type'])}"), "grey")
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback("give-hash-verbose", f"indeed, h({white_string}) = {hash_value(white_string,ENV['hash_type'])}"), "yellow", ["underline"])
        exit(0)
    
exit(0)
