#!/usr/bin/env python3
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import chococroc_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="chococroc"
service="check_game_value"

args_list = [
    ('m',int),
    ('n',int),
    ('value',int),
    ('silent',bool)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'delayed' if ENV['silent'] else 'now')

# START CODING YOUR SERVICE:
grundy_val = cl.grundy_val(ENV['m'], ENV['n'])
#print(f"grundy_val={grundy_val}")
if ENV['value'] == -2: # user conjectures this is a first_to_move_wins position
    if grundy_val == 0:
        TAc.print(LANG.render_feedback("not-a-winning-conf", f'No! Contrary to your conjecture, the configuration {ENV["m"]} x {ENV["n"]} is NOT a winning one.'), "red")
        TAc.print(LANG.render_feedback("not-a-winning-conf-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on configuration {ENV["m"]} x {ENV["n"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-winning-conf", f'Ok! We agree with your conjecture that the configuration {ENV["m"]} x {ENV["n"]} is a winning one.'), "green", ["bold"])

if ENV['value'] == -1: # user conjectures this is a first_to_move_loses position
    if grundy_val != 0:
        TAc.print(LANG.render_feedback("not-a-lost-conf", f'No! Contrary to your conjecture, the configuration {ENV["m"]} x {ENV["n"]} is NOT a lost one.'), "red")
        TAc.print(LANG.render_feedback("not-a-lost-conf-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from configuration {ENV["m"]} x {ENV["n"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-lost-conf", f'Ok! We agree with your conjecture that the configuration {ENV["m"]} x {ENV["n"]} is a lost one.'), "green", ["bold"])

if ENV['value'] >= 0:  # user conjectures that the Grundy value of the position ENV["number"] is ENV['value']
    if grundy_val != ENV['value']:
        TAc.print(LANG.render_feedback("wrong-grundy-val", f'No! Contrary to your conjecture, the grundy value of configuration {ENV["m"]} x {ENV["n"]} is NOT {ENV["value"]}.'), "red")
        if grundy_val * ENV['value'] != 0:
            TAc.print(LANG.render_feedback("wrong-grundy-val-play", f'You can check this out playing a game against our service \'play_val_measuring_game\', starting second on configuration (chocolate_bar={ENV["m"]} x {ENV["n"]}, single_NIM_tower={ENV["value"]}). If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        elif grundy_val == 0:
            TAc.print(LANG.render_feedback("not-a-winning-conf", f'Indeed, the configuration {ENV["m"]} x {ENV["n"]} is NOT a winning one for the first player to move.'), "red")
            TAc.print(LANG.render_feedback("not-a-winning-conf-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on configuration {ENV["m"]} x {ENV["n"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        else:    
            TAc.print(LANG.render_feedback("not-a-lost-conf", f'Indeed, the configuration {ENV["m"]} x {ENV["n"]} is NOT a lost one for the first player to move.'), "red")
            TAc.print(LANG.render_feedback("not-a-lost-conf-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from configuration {ENV["m"]} x {ENV["n"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-grundy-val", f'Ok! We agree with your conjecture that the configuration {ENV["m"]} x {ENV["n"]} has grundy value {grundy_val}.'), "green", ["bold"])

exit(0)
