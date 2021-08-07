#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_rank"
args_list = [
    ('input_treatment',str),
    ('rank',int),
    ('sorting_criterion',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV["input_treatment"], TAc, LANG, yield_feedback=False) or not ENV["silent"]:
    TAc.print(LANG.opening_msg, "green")
    if not recognize(ENV["input_treatment"], TAc, LANG):
        exit(0)

n_pills = len(ENV["input_treatment"])//2 
p = Flask(n_pills)
      
if ENV["rank"] == p.rank(ENV["input_treatment"],sorting_criterion=ENV["sorting_criterion"]):
    if not ENV["silent"]:
        TAc.OK()
        print(LANG.render_feedback("rank-ok", f'♥  You correctly ranked the treatment among those on {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'))
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
if ENV["rank"] < p.rank(ENV["input_treatment"],sorting_criterion=ENV["sorting_criterion"]):
    TAc.print(LANG.render_feedback("ranked-too-low", f'No. Your treatment ranks higher than {ENV["rank"]} among those with {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
if ENV["rank"] > p.rank(ENV["input_treatment"],sorting_criterion=ENV["sorting_criterion"]):
    TAc.print(LANG.render_feedback("ranked-too-high", f'No. Your treatment ranks lower than {ENV["rank"]} among those with {n_pills} pills (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
exit(0)
