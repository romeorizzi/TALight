#!/usr/bin/env python3
from sys import stderr, exit, argv
from random import randrange

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('num_questions',int),
    ('numbers',str),
    ('META_TTY',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE: 

LANG.print_opening_msg()
gen_new_pair = True    
for _ in range(ENV['num_questions']):
    if gen_new_pair:
        if ENV['numbers'] == "onedigit":
            x = randrange(10)
            y = randrange(10)
        elif ENV['numbers'] == "twodigits":
            x = randrange(100)
            y = randrange(100)
        else:
            x = randrange(2**64)
            y = randrange(2**64)
    if x < y:
        x,y = y,x
    TAc.print(f"{x+y} {x-y}", "yellow", ["bold"])
    TAc.print(f"SERVER: {x+y} {x-y}", "yellow", ["bold"], file=stderr)
    a, b = TALinput(int, 2, TAc=TAc)
    gen_new_pair = False
    if a+b > x+y:
        TAc.NO()
        TAc.print(f"# No!", "red", ["bold"], end="", file=stderr)
        TAc.print(LANG.render_feedback("over-sum", f"indeed, {a}+{b}={a+b} > {x+y}."), "yellow", ["underline"])
        TAc.print(LANG.render_feedback("over-sum", f"indeed, {a}+{b}={a+b} > {x+y}."), "yellow", ["underline"], file=stderr)
    elif a+b < x+y:    
        TAc.NO() 
        TAc.print(f"# No!", "red", ["bold"], end="", file=stderr)
        TAc.print(LANG.render_feedback("under-sum", f"indeed, {a}+{b}={a+b} < {x+y}."), "yellow", ["underline"])
        TAc.print(LANG.render_feedback("under-sum", f"indeed, {a}+{b}={a+b} < {x+y}."), "yellow", ["underline"], file=stderr)
    elif abs(a-b) > x-y:    
        TAc.NO() 
        TAc.print(f"# No!", "red", ["bold"], end="", file=stderr)
        TAc.print(LANG.render_feedback("too-apart", f"indeed, |{a}-{b}|={abs(a-b)} > {x-y}."), "yellow", ["underline"])
        TAc.print(LANG.render_feedback("too-apart", f"indeed, |{a}-{b}|={abs(a-b)} > {x-y}."), "yellow", ["underline"], file=stderr)
    elif abs(a-b) < x-y:    
        TAc.NO() 
        TAc.print(f"# No!", "red", ["bold"], end="", file=stderr)
        TAc.print(LANG.render_feedback("too-close", f"indeed, |{a}-{b}|={abs(a-b)} < {x-y}."), "yellow", ["underline"])
        TAc.print(LANG.render_feedback("too-close", f"indeed, |{a}-{b}|={abs(a-b)} < {x-y}."), "yellow", ["underline"], file=stderr)
    else:
        TAc.OK() 
        TAc.print(f"# YES!", "green", ["bold"], end="", file=stderr)
        assert (a + b == x+y) and (abs(a-b) == x-y)
        TAc.print(LANG.render_feedback("ok", f"indeed, {a}+{b} = {x+y} and |{a}-{b}| = {x-y}."), "grey")
        TAc.print(LANG.render_feedback("ok", f"indeed, {a}+{b} = {x+y} and |{a}-{b}| = {x-y}."), "grey", file=stderr)
        gen_new_pair = True

TAc.Finished()
exit(0)
