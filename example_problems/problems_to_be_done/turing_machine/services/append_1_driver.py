#!/usr/bin/env python3
from sys import stderr, exit
from random import randrange
from os import environ
from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
import random
import turing_machine_lib as tr
# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('max_lengh',int),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE: 
LANG.print_opening_msg()
sequence = tr.random_seq(ENV['seed'], ENV['max_lengh'])

#TAc.print(LANG.render_feedback("instance-seed",f"Instance (of seed {seed}): "), "yellow", ["bold"])
print("Sequence")
for i in sequence:
    print(i, end="")
print()
#TAc.print(LANG.render_feedback("long-sol","Too long solution: "), "yellow", ["bold"])
#catch input while the string isn't q
text = ""
while True:
    line = input()
    if line == 'stop':
        break
    text += (line + "\n")
print()
print("Your solution:")
print(text)
rules = tr.getRules(text)
print()
print("Rules:")
print(rules)
 
exit(0)