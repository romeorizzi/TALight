#!/usr/bin/env python3
from sys import stderr, exit, argv

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_unrank"
args_list = [
    ('input_rank',int),
    ('formula',str),
    ('sorting_criterion',str),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV['formula'], TAc, LANG, yield_feedback=False):
    ENV['silent'] = False
if not ENV['silent']:
    TAc.print(LANG.opening_msg, "green")
    if not recognize(ENV['input_formula'], TAc, LANG):
        exit(0)

n_pairs = len(ENV['formula'])//2
p = Par(n_pairs)

if ENV['formula'] == p.unrank(n_pairs,ENV['input_rank'], sorting_criterion=ENV['sorting_criterion']):
    if not ENV['silent']:
        TAc.OK()
        print(LANG.render_feedback("rank-ok", f"♥  You correctly ranked the formula among those on {len(ENV['formula'])//2} pairs of parentheses (when sorted according to sorting_criterion={ENV['sorting_criterion']})."))
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
if ENV['input_rank'] < p.rank(ENV['formula'], sorting_criterion=ENV['sorting_criterion']):
    TAc.print(LANG.render_feedback("ranks-higher", f"No. Your formula ranks higher than {ENV['input_rank']} among those with {len(ENV['formula'])//2} pairs of parentheses (when sorted according to sorting_criterion={ENV['sorting_criterion']})."), "red", ["bold"])
if ENV['input_rank'] > p.rank(ENV['formula'], sorting_criterion=ENV['sorting_criterion']):
    TAc.print(LANG.render_feedback("ranks-lower", f"No. Your formula ranks lower than {ENV['input_rank']} among those with {len(ENV['formula'])//2} pairs of parentheses (when sorted according to sorting_criterion={ENV['sorting_criterion']})."), "red", ["bold"])
exit(0)
