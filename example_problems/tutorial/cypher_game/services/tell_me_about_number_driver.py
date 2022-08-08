#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import cypher_game_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="cypher_game"
service="tell_me_about_number"
args_list = [
    ('number',int),
    ('info_requested',str),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
info_requested = ENV['info_requested']
lang = ENV['lang']

grundy_val = cl.grundy_val(ENV['number'])

if(info_requested=="won_or_lost"):
    if(grundy_val>0):
        TAc.print(LANG.render_feedback("is-winning-numb", f'Your number \'{ENV["number"]}\' is a winning one'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("is-lost-numb", f'Your number \'{ENV["number"]}\' is a lost one'), "yellow", ["bold"])

elif(info_requested=="grundy_val"):
    TAc.print(LANG.render_feedback("grundy-val-numb", f'Your number \'{ENV["number"]}\' has grundy value = {grundy_val}'), "yellow", ["bold"])

elif(info_requested=="gimme_a_winning_move"):
    if (grundy_val>0):
        TAc.print(LANG.render_feedback("one-winning-move-numb", f'One of the possible winning moves for your number \'{ENV["number"]}\' is \'{cl.find_winning_move(ENV["number"])[0]}\''), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no-winning-move-numb", f'Your number \'{ENV["number"]}\' is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])

exit(0)