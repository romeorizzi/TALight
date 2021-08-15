#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="gimme_next_sol"
args_list = [
    ('current_sol',str),
    ('sorting_criterion',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV["current_sol"], TAc, LANG)
    exit(0)
n_pairs = len(ENV["current_sol"])//2 
p = Par(n_pairs)
if p.rank(ENV["current_sol"], sorting_criterion=ENV["sorting_criterion"]) == p.num_sol(n_pairs) -1:
    TAc.print("Be told that your formula is the very last in the list", "yellow")
else:
    TAc.print(p.unrank(n_pairs, 1+p.rank(ENV["current_sol"], sorting_criterion=ENV["sorting_criterion"]), sorting_criterion=ENV["sorting_criterion"]), "yellow", ["bold"])

exit(0)
