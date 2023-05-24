#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import game_parenthesis_lib as pl

# METADATA OF THIS TAL_SERVICE:
problem="game-parenthesis"
service="check_game_value"

args_list = [
    ('formula',str),
    ('value',int),
    ('silent',bool)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'delayed' if ENV['silent'] else 'now')

# START CODING YOUR SERVICE:
if not pl.recognize(ENV['formula'], TAc, LANG):
    exit(0)
grundy_val = pl.grundy_val(ENV['formula'])
#print(f"grundy_val={grundy_val}")
if ENV['value'] == -2: # user conjectures this is a first_to_move_wins position
    if grundy_val == 0:
        TAc.print(LANG.render_feedback("not-a-winning-form", f'No! Contrary to your conjecture, the formula \'{ENV["formula"]}\' is NOT a winning one.'), "red")
        TAc.print(LANG.render_feedback("not-a-winning-form-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on formula \'{ENV["formula"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-winning-form", f'Ok! We agree with your conjecture that the formula \'{ENV["formula"]}\' is a winning one.'), "green", ["bold"])

if ENV['value'] == -1: # user conjectures this is a first_to_move_loses position
    if grundy_val != 0:
        TAc.print(LANG.render_feedback("not-a-lost-form", f'No! Contrary to your conjecture, the formula \'{ENV["formula"]}\' is NOT a lost one.'), "red")
        TAc.print(LANG.render_feedback("not-a-lost-form-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from formula \'{ENV["formula"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-lost-form", f'Ok! We agree with your conjecture that the formula \'{ENV["formula"]}\' is a lost one.'), "green", ["bold"])

if ENV['value'] >= 0:  # user conjectures that the Grundy value of the position ENV["number"] is ENV['value']
    if grundy_val != ENV['value']:
        TAc.print(LANG.render_feedback("wrong-grundy-val-form", f'No! Contrary to your conjecture, the grundy value of the formula \'{ENV["formula"]}\' is NOT {ENV["value"]}.'), "red")
        if grundy_val * ENV['value'] != 0:
            TAc.print(LANG.render_feedback("wrong-grundy-val-play-form", f'You can check this out playing a game against our service \'play_val_measuring_game\', starting second on formula (formula=\'{ENV["formula"]}\', single_NIM_tower={ENV["value"]}). If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        elif grundy_val == 0:
            TAc.print(LANG.render_feedback("not-a-winning-form", f'Indeed, the formula \'{ENV["formula"]}\' is NOT a winning one for the first to move.'), "red")
            TAc.print(LANG.render_feedback("not-a-winning-form-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on formula \'{ENV["formula"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
        else:    
            TAc.print(LANG.render_feedback("not-a-lost-form", f'Indeed, the formula \'{ENV["formula"]}\' is NOT a lost one for the first to move.'), "red")
            TAc.print(LANG.render_feedback("not-a-lost-form-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from formula \'{ENV["formula"]}\'. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.print(LANG.render_feedback("ok-grundy-val-form", f'Ok! We agree with your conjecture that the formula \'{ENV["formula"]}\' has grundy value {grundy_val}.'), "green", ["bold"])

exit(0)
