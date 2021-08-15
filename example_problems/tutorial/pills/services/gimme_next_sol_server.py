#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
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
n_pills = len(ENV["current_sol"])//2 
p = Flask(n_pills)
if p.rank(ENV["current_sol"], sorting_criterion=ENV["sorting_criterion"]) == p.num_sol(n_pills) -1:
    TAc.print("Be told that your treatment is the very last in the list", "yellow")
else:
    TAc.print(p.unrank(n_pills, 1+p.rank(ENV["current_sol"], sorting_criterion=ENV["sorting_criterion"]), sorting_criterion=ENV["sorting_criterion"]), "yellow", ["bold"])

exit(0)
