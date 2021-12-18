#!/usr/bin/env python3
import sys

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import chococroc_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="tell_me_about_config"
args_list = [
    ('m',int),
    ('n',int),
    ('info_requested',str),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
info_requested = ENV['info_requested']
lang = ENV['lang']

grundy_val = cl.grundy_val(ENV["m"], ENV['n'])

if(info_requested=="won_or_lost"):
    if(grundy_val>0):
        TAc.print(LANG.render_feedback("is-winning", f'Your configuration {ENV["m"]} x {ENV["n"]} is a winning one'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("is-lost", f'Your configuration {ENV["m"]} x {ENV["n"]} is a lost one'), "yellow", ["bold"])

elif(info_requested=="grundy_val"):
    TAc.print(LANG.render_feedback("grundy-val", f'Your configuration {ENV["m"]} x {ENV["n"]} has grundy value = {grundy_val}'), "yellow", ["bold"])

elif(info_requested=="gimme_a_winning_move"):
    if (grundy_val>0):
        TAc.print(LANG.render_feedback("one-winning-move", f'One of the possible winning moves for your configuration {ENV["m"]} x {ENV["n"]} is {cl.winning_move(ENV["m"], ENV["n"])}'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no-winning-move", f'Your configuration {ENV["m"]} x {ENV["n"]} is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])
        
elif(info_requested=="gimme_all_winning_moves"):
    if (grundy_val>0):
        TAc.print(LANG.render_feedback("all-winning-moves", f'The possible winning moves for your configuration {ENV["m"]} x {ENV["n"]} are {cl.winning_moves(ENV["m"], ENV["n"])}'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("no-winning-move", f'Your configuration {ENV["m"]} x {ENV["n"]} is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])


exit(0)
