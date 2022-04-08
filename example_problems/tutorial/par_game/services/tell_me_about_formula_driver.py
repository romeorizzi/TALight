#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import par_game_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="par_game"
service="tell_me_about_formula"
args_list = [
    ('formula',str),
    ('info_requested',str),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
if not pl.recognize(ENV['formula'], TAc, LANG):
    exit(0)
info_requested = ENV['info_requested']
lang = ENV['lang']

grundy_val = pl.grundy_val(ENV['formula'])

if(info_requested=="won_or_lost"):
    if(grundy_val>0):
        TAc.print(LANG.render_feedback("is-winning-form", f'Your formula \'{ENV["formula"]}\' is a winning one'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("is-lost-form", f'Your formula \'{ENV["formula"]}\' is a lost one'), "yellow", ["bold"])

elif(info_requested=="grundy_val"):
    TAc.print(LANG.render_feedback("grundy-val-form", f'Your formula \'{ENV["formula"]}\' has grundy value = {grundy_val}'), "yellow", ["bold"])

elif(info_requested=="gimme_a_winning_move"):
    if (grundy_val>0):
        TAc.print(LANG.render_feedback("one-winning-move-form", f'One of the possible winning moves for your formula \'{ENV["formula"]}\' is \'{pl.find_move_par_game(ENV["formula"])}\''), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no-winning-move-form", f'Your formula \'{ENV["formula"]}\' is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])
        
elif(info_requested=="gimme_all_winning_moves"):
    if (grundy_val>0):
        TAc.print(LANG.render_feedback("all-winning-moves-form", f'The possible winning moves for your formula \'{ENV["formula"]}\' are {pl.find_moves_par_game(ENV["formula"], True)}'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no-winning-move-form", f'Your formula \'{ENV["formula"]}\' is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])


exit(0)