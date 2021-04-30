#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="gimme_rank"
args_list = [
    ('formula',str),
    ('sorting_criterion',str),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV['formula'], TAc, LANG, yield_feedback=False):
    TAc.print(LANG.opening_msg, "green")
    recognize(ENV['formula'], TAc, LANG)
    exit(0)
n_pairs = len(ENV['formula'])//2 
p = Par(n_pairs)
TAc.print(p.rank(ENV['formula'],sorting_criterion=ENV['sorting_criterion'])+1, "yellow", ["bold"])

exit(0)
