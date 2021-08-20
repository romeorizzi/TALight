#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="gimme_rank"
args_list = [
    ('treatment',str),
    ('sorting_criterion',str),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV['treatment'], TAc, LANG)
    exit(0)
n_pills = len(ENV['treatment'])//2 
p = Flask(n_pills)
TAc.print(p.rank(ENV['treatment'],sorting_criterion=ENV['sorting_criterion']), "yellow", ["bold"])

exit(0)
