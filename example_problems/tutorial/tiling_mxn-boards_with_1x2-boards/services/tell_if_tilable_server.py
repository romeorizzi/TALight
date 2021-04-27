#!/usr/bin/env python3
from sys import stderr, exit, argv
from random import randrange

#from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
problem="tiling_mxn-boards_with_1x2-boards"
service="is_tilable"
args_list = [
    ('m',int),
    ('n',int),
    ('my_conjecture',str),
    ('h',int),
    ('k',int),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE: 

assert ENV['h']==1
assert ENV['k']==2

print()

if (ENV['m'] * ENV['n']) % 2 == 1:
    if ENV['my_conjecture'] == "yes":
        TAc.NO() 
        print(LANG.render_feedback("FALSE-is-not-tilable", f"Contrary to what you have asserted, the {ENV['m']}x{ENV['n']}-grid is NOT tilable. If you are not convinced you can submit a tiling of that grid to the service 'check_my_tiling'."))
    if ENV['my_conjecture'] == "no":
        TAc.OK() 
        print(LANG.render_feedback("TRUE-is-not-tilable", f"You are perfecty right: the {ENV['m']}x{ENV['n']}-grid is NOT tilable."))
        
if (ENV['m'] * ENV['n']) % 2 == 0:
    if ENV['my_conjecture'] == "yes":
        TAc.OK() 
        print(LANG.render_feedback("TRUE-is-tilable", f"We agree on the fact that the {ENV['m']}x{ENV['n']}-grid is tilable. If you want to exhibit us a tiling for this grid you can submit it to the service 'check_my_tiling'."))
    if ENV['my_conjecture'] == "no":
        TAc.NO() 
        print(LANG.render_feedback("FALSE-is-tilable", f"No, the {ENV['m']}x{ENV['n']}-grid is tilable. If you can not believe a tiling of the {ENV['m']}x{ENV['n']}-grid exists try the service 'gimme_hints_on_a_tiling'."))

exit(0)
