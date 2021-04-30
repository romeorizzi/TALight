#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, TALcolors

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_unrank"
args_list = [
    ('n_pairs',int),
    ('rank',int),
    ('sorting_criterion',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)

# START CODING YOUR SERVICE:
p = Par(ENV['n_pairs'])
TAc.print(p.unrank(ENV['n_pairs'],ENV['rank']-1,sorting_criterion=ENV['sorting_criterion']), "yellow", ["bold"])

exit(0)
