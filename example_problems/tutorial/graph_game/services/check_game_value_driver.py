#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_game_lib as gl

# METADATA OF THIS TAL_SERVICE:
problem="graph_game"
service="check_game_value"

args_list = [
    ('graph',str),
    ('starting_node',int),
    ('value',int),
    ('silent',bool)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
graph=gl.generate_graph_from_input(ENV['graph'])
f_player_w = gl.first_player_win(graph)
moves=gl.find_winning_moves_on_graph_not_winning(graph,ENV['starting_node'],True)
#print(f"grundy_val={grundy_val}")
if ENV['value'] == -2:
    if not(f_player_w) and moves==[]:
        TAc.NO()
        TAc.print(LANG.render_feedback("not-a-winning-graph", f'Contrary to your conjecture, the graph \'{ENV["graph"]}\' is NOT a winning one.'), "red")
        TAc.print(LANG.render_feedback("not-a-winning-graph-wanna-play", f'You can check this out playing a game against our service \'play\', starting first on graph \'{ENV["graph"]}\' from node {ENV["starting_node"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok-winning-graph", f'We agree with your conjecture that the graph \'{ENV["graph"]}\' is a winning one.'), "green", ["bold"])

if ENV['value'] == -1:
    if f_player_w or moves!=[]:
        TAc.NO()
        TAc.print(LANG.render_feedback("not-a-lost-graph", f'Contrary to your conjecture, the graph \'{ENV["graph"]}\' is NOT a lost one.'), "red")
        TAc.print(LANG.render_feedback("not-a-lost-graph-wanna-play", f'You can check this out playing a game against our service \'play\', playing as second a game starting from graph \'{ENV["graph"]}\' from node {ENV["starting_node"]}. If you succeed winning then you disprove our claim or the optimality of our player (either way, let us know).'), "yellow", ["bold"])
    elif not ENV['silent']:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok-lost-graph", f'We agree with your conjecture that the graph \'{ENV["graph"]}\' is a lost one.'), "green", ["bold"])

exit(0)