#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, TALcolors

from pills_lib import recognize, Flask

# METADATA OF THIS TAL_SERVICE:
problem="pills"
service="check_unrank"
args_list = [
    ('n_pills',int),
    ('rank',int),
    ('sorting_criterion',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)

# START CODING YOUR SERVICE:
p = Flask(ENV['n_pills'])
TAc.print(p.unrank(ENV['n_pills'],ENV['rank'],sorting_criterion=ENV['sorting_criterion']), "yellow", ["bold"])

exit(0)
