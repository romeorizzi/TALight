#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors

from math_modeling import ModellingProblemHelper

import asteroid_lib as ll


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('display_output',bool),
    ('display_error',bool),
    ('format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:

mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))

if ENV['format'] == 'math':
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (ef=your_ef_file dat=your_dat_file.dat)."), "yellow")

    mph.receive_ef_file()
    mph.receive_dat_file()
else:
    TAc.print(LANG.render_feedback("start", f"# Hey, I am ready to start and get your input files (ef=your_ef_file)."), "yellow")

    mph.receive_ef_file()

mph.run_ef_GLPSOL(ENV['format'])

glpsol_output = mph.get_out_str()

if ENV['display_output']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    TAc.print(LANG.render_feedback("out-title", "The GLPSOL stdout is: "), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("stdout", f"{glpsol_output}"), "white", ["reverse"])

if glpsol_output.find("NO PRIMAL") != -1:
    TAc.print(LANG.render_feedback('error-no-sol', f'#ERROR: Your model does not generate a solution.'), 'red', ['bold'])
    exit(0)

if ENV['display_error']:
    TAc.print(LANG.render_feedback("separator", "<================>"), "yellow", ["reverse"])
    glpsol_error = mph.get_err_str()
    TAc.print(LANG.render_feedback("err-title", "The GLPSOL stderr is: "), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("stderr", f"{glpsol_error}"), "white", ["reverse"])

exit(0)
