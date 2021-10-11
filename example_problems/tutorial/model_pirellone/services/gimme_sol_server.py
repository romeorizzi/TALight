#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

import pirellone_lib as pl
from utils_services import process_instance

# METADATA OF THIS TAL_SERVICE:
problem="model_pirellone"
service="gimme_sol"
args_list = [
    ('input_mode',str),
    ('m',int), 
    ('n',int),
    ('seed',str),
    ('sol_style',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
# Get pirellone and solution
(instance, opt_sol) = process_instance(ENV, TAc, LANG)
# TAc.print(LANG.render_feedback("solution-title", f"{pl.sol_to_str(instance, opt_sol)}"), "green", ["bold"])

# Print solution
TAc.print(LANG.render_feedback("solution-title", f"The optimal solution for this instance is:"), "green", ["bold"])
if ENV['sol_style'] == 'seq':
    TAc.print(LANG.render_feedback("legend-seq", f"(r=row, c=col)"), "white", ["bold"])
    TAc.print(LANG.render_feedback("solution", f"{pl.seq_to_str(pl.subset_to_seq(opt_sol))}"), "white", ["reverse"])
elif ENV['sol_style'] == 'subset':
    TAc.print(LANG.render_feedback("legend-subset", f"(FirstLine=rows_switch SecondLine=cols_switch)"), "white", ["bold"])
    sol_str = pl.subset_to_str_list(opt_sol)
    # TAc.print(LANG.render_feedback("rows", f"Rows: {sol_str[0]}"), "white", ["reverse"])
    # TAc.print(LANG.render_feedback("cols", f"Cols: {sol_str[1]}"), "white", ["reverse"])
    TAc.print(LANG.render_feedback("solution", f"{pl.subset_to_str(opt_sol)}"), "white", ["reverse"])

exit(0)
