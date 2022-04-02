#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('silent',bool),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

#CHECK MIN_VAL <= MAX_VAL

if ENV['MIN_VAL'] > ENV['MAX_VAL']:
    TAc.NO()
    TAc.print(LANG.render_feedback("range-is-empty", f"Error: I can not choose the integers for the triangle from the range [{MIN_VAL},{MAX_VAL}] since this range is empty.", {"MIN_VAL":MIN_VAL, "MAX_VAL":MAX_VAL}), "red", ["bold"])
    exit(0)

# START CODING YOUR SERVICE:

# Get Triangle
instance = tl.random_triangle(ENV['n'], ENV['MIN_VAL'], ENV['MAX_VAL'], ENV['seed'])

# Print Instance
if ENV['silent']:
    tl.print_triangle(instance)
else:
    TAc.print(LANG.render_feedback("show_instance", f"Here is your pseudo-random triangle (<n={ENV['n']},MIN_VAL={ENV['MIN_VAL']},MAX_VAL={ENV['MAX_VAL']},seed={ENV['seed']}>):"), "yellow", ["bold"])
    tl.print_triangle(instance)

exit(0)
