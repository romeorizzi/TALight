#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_unrank"
args_list = [
    ('input_rank',int),
    ('treatment',str),
    ('sorting_criterion',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV["treatment"], TAc, LANG, yield_feedback=False) or not ENV["silent"]:
    TAc.print(LANG.opening_msg, "green")
    if not recognize(ENV["treatment"], TAc, LANG):
        exit(0)

n_pills = len(ENV["treatment"])//2
p = Flask(n_pills)

if ENV["treatment"] == p.unrank(n_pills,ENV["input_rank"], sorting_criterion=ENV["sorting_criterion"]):
    if not ENV["silent"]:
        TAc.OK()
        print(LANG.render_feedback("rank-ok", f'♥  Correct! It is indeed this one the treatment that appears with rank={ENV["input_rank"]} among the feasible treatments on {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'))
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
if ENV["input_rank"] < p.rank(ENV["treatment"], sorting_criterion=ENV["sorting_criterion"]):
    TAc.print(LANG.render_feedback("ranks-higher", f'No. Your treatment ranks higher than {ENV["input_rank"]} among those with {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
if ENV["input_rank"] > p.rank(ENV["treatment"], sorting_criterion=ENV["sorting_criterion"]):
    TAc.print(LANG.render_feedback("ranks-lower", f'No. Your treatment ranks lower than {ENV["input_rank"]} among those with {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
exit(0)
