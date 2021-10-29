#!/usr/bin/env python3
from sys import stderr, exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput

from piastrelle_lib import Par

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('current_sol',str),
    ('next_sol',str),
    ('sorting_criterion',str),
    ('tell_maximal_correct_feedback',bool),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
current_sol=ENV['current_sol']
len_lines=len(ENV['current_sol'])
next_sol=ENV['next_sol']
n_tiles=len_lines//2
p = Par(n_tiles)
if not len(next_sol) == len_lines:
    TAc.print(LANG.render_feedback("different_lengths", f"No. The tiling introduced in 'next_sol' is different in length from the 'current_sol'."), "red", ["bold"])
    exit(0)
if next_sol == current_sol:
    TAc.print(LANG.render_feedback("repeated", f"No. The tiling you introduced in 'next_sol' is the same as the 'current_sol'."), "red", ["bold"])
    exit(0)

def max_corr_feedback(lista):
    min_len = 0
    while next_sol[min_len] == lista[min_len]:
        min_len += 1
    if not min_len==1:
        TAc.print(LANG.render_feedback("repeated", f"The tiling {next_sol} is right only for the prefix{next_sol[:min_len-1]}."), "red", ["bold"])
    else:
        TAc.print(LANG.render_feedback("repeated", f"The tiling {next_sol} has no prefix in common with the next solution of {current_sol}."), "red", ["bold"])

pos=p.rank(current_sol,ENV['sorting_criterion'])
if pos+1 != p.num_sol(n_tiles) and next_sol != p.unrank(n_tiles,pos+1,ENV['sorting_criterion']):
    TAc.print(LANG.render_feedback("repeated", f"No. The tiling {next_sol} is not the next of {current_sol}. (The service was called with 'sorting_criterion'={ENV['sorting_criterion']})"), "red", ["bold"])
    if ENV['tell_maximal_correct_feedback']:
        max_corr_feedback(p.unrank(n_tiles,pos+1,ENV['sorting_criterion']))
    exit(0)
elif pos == p.num_sol(n_tiles)-1:
    TAc.print(LANG.render_feedback("repeated", f"No. The tiling {next_sol} is not the next of {current_sol}. (The service was called with 'sorting_criterion'={ENV['sorting_criterion']})"), "red", ["bold"])
    if ENV['tell_maximal_correct_feedback']:
        TAc.print(LANG.render_feedback("repeated", f"The tiling {current_sol} is already the last you can enter."), "red", ["bold"])
    exit(0)

TAc.print(LANG.render_feedback("list-ok", f"Ok! You have listed two consecutive tilings of a corridor of dimension 1x{n_tiles}."), "green", ["bold"])
exit(0)
