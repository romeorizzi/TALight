#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from parentheses_lib import recognize, Par

# METADATA OF THIS TAL_SERVICE:
problem="parentheses"
service="check_rank"
args_list = [
    ('input_formula',str),
    ('rank',int),
    ('sorting_criterion',str),
    ('more_or_less_hint_if_wrong',bool),
    ('silent',bool),
    ('lang',str),
    ('ISATTY',bool),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
answ=ENV["rank"]
input_form=ENV["input_formula"]
if not recognize(input_form, TAc, LANG, yield_feedback=False) or not ENV["silent"]:
    TAc.print(LANG.opening_msg, "green")
    if not recognize(input_form, TAc, LANG):
        exit(0)

n_pairs = len(input_form)//2 
p = Par(n_pairs)
      
if answ == p.rank(input_form,sorting_criterion=ENV["sorting_criterion"])+1:
    if not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("rank-ok", f':)  You correctly ranked the formula among those on {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'),"green",["bold"])
    exit(0)

# INDEPTH NEGATIVE FEEDBACK:
if answ < p.rank(input_form,sorting_criterion=ENV["sorting_criterion"])+1 and ENV["more_or_less_hint_if_wrong"]:
    TAc.print(LANG.render_feedback("ranked-too-low", f'No. Your formula ranks higher than {answ} among those with {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
    exit(0)
if answ > p.rank(input_form,sorting_criterion=ENV["sorting_criterion"])+1 and ENV["more_or_less_hint_if_wrong"]:
    TAc.print(LANG.render_feedback("ranked-too-high", f'No. Your formula ranks lower than {answ} among those with {n_pairs} pairs of parentheses (when sorted according to sorting_criterion={ENV["sorting_criterion"]}).'), "red", ["bold"])
    exit(0)
TAc.print(LANG.render_feedback("risp-no", f"No, {answ} is not the position of {input_form} in the list of {n_pairs} pairs of parentheses."), "red", ["bold"])
exit(0)
