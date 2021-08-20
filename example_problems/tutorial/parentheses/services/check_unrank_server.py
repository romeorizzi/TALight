#!/usr/bin/env python3
from sys import stderr, exit

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
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not recognize(ENV["formula"], TAc, LANG):
    exit(0)

n_pairs = len(ENV["formula"])//2
p = Par(n_pairs)
rank=ENV["input_rank"]-1
crit=ENV["sorting_criterion"]
if ENV["formula"] == p.unrank(n_pairs,rank, sorting_criterion=crit):
    if not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("rank-ok", f':)  Correct! It is indeed this one the formula that appears with rank={rank+1} among the well formed formulas on {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={crit}).'),"green",["bold"])
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
if rank < p.rank(ENV["formula"], sorting_criterion=crit) and ENV["more_or_less_hint_if_wrong"]:
    TAc.print(LANG.render_feedback("ranks-higher", f'No. Your formula ranks higher than {rank+1} among those with {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={crit}).'), "red", ["bold"])
    exit(0)
if rank > p.rank(ENV["formula"], sorting_criterion=crit) and ENV["more_or_less_hint_if_wrong"]:
    TAc.print(LANG.render_feedback("ranks-lower", f'No. Your formula ranks lower than {rank+1} among those with {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={crit}).'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("risp-no", f"No. Your formula does not rank {rank+1} among those with {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={crit})."), "red", ["bold"])
exit(0)
