#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import cypher_game_lib as cl

# METADATA OF THIS TAL_SERVICE:
problem="cypher_game"
service="check_game_value"

args_list = [
    ('number',int),
    ('value',int),
    ('silent',bool)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'delayed' if ENV['silent'] else 'now')

# START CODING YOUR SERVICE:
grundy_val = cl.grundy_val(ENV['number'])
#print(f"grundy_val={grundy_val}")
if ENV['value'] == -2: # user conjectures this is a first_to_move_wins position
    if grundy_val == 0:
        TAc.print(LANG.render_feedback("not-a-winning-numb", f'No! Contrary to your conjecture, the number \'{ENV["number"]}\' is NOT a winning one.'), "red")
        TAc.print(LANG.render_feedback("not-a-winning-numb-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on number \'{ENV["number"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-winning-numb", f'Yes! We agree with your conjecture that the number \'{ENV["number"]}\' is a winning one.'), "green", ["bold"])

if ENV['value'] == -1: # user conjectures this is a first_to_move_loses position
    if grundy_val != 0:
        TAc.print(LANG.render_feedback("not-a-lost-numb", f'No! Contrary to your conjecture, the number \'{ENV["number"]}\' is NOT a lost one.'), "red")
        TAc.print(LANG.render_feedback("not-a-lost-numb-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from number \'{ENV["number"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-lost-numb", f'Yes. We agree with your conjecture that the number \'{ENV["number"]}\' is a lost one.'), "green", ["bold"])

if ENV['value'] >= 0:  # user conjectures that the Grundy value of the position ENV["number"] is ENV['value']
    if grundy_val != ENV['value']:
        TAc.print(LANG.render_feedback("wrong-grundy-val-numb", f'No! Contrary to your conjecture, the grundy value of the number \'{ENV["number"]}\' is NOT {ENV["value"]}.'), "red")
        if grundy_val * ENV['value'] != 0:
            TAc.print(LANG.render_feedback("wrong-grundy-val-play-numb", f'You can check this out playing a game against our service \'play_val_measuring_game\', starting second on number (number=\'{ENV["number"]}\', single_NIM_tower={ENV["value"]}). If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        elif grundy_val == 0:
            TAc.print(LANG.render_feedback("not-a-winning-numb", f'Indeed, the number \'{ENV["number"]}\' is NOT a winning one for the first to move.'), "red")
            TAc.print(LANG.render_feedback("not-a-winning-numb-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on number \'{ENV["number"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        else:    
            TAc.print(LANG.render_feedback("not-a-lost-numb", f'Indeed, the number \'{ENV["number"]}\' is NOT a lost one.'), "red")
            TAc.print(LANG.render_feedback("not-a-lost-numb-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from number \'{ENV["number"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-grundy-val-numb", f'Yes. We agree with your conjecture that the number \'{ENV["number"]}\' has grundy value {grundy_val}.'), "green", ["bold"])

exit(0)
