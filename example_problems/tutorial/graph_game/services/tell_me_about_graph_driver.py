#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import graph_game_lib as gl

# METADATA OF THIS TAL_SERVICE:
problem="graph_game"
service="tell_me_about_graph"
args_list = [
    ('graph',str),
    ('starting_node',int),
    ('info_requested',str),
    ('lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
info_requested = ENV['info_requested']
lang = ENV['lang']

graph=gl.generate_graph_from_input(ENV['graph'])
if not(ENV['starting_node'] in gl.get_nodes(graph)):
    TAc.print(LANG.render_feedback("graph-illegal-start-node", '# We have a problem. The starting node is not valid because is not a node of the graph.'), "red", ["bold"])
    exit(0)
#print(gl.get_edges(graph))
f_player_w = gl.first_player_win(graph)

if(info_requested=="won_or_lost"):
    if f_player_w:
        TAc.print(LANG.render_feedback("is-winning-graph", f'Your graph \'{ENV["graph"]}\' is a winning one'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("is-lost-graph", f'Your graph \'{ENV["graph"]}\' is a lost one'), "yellow", ["bold"])

elif(info_requested=="gimme_a_winning_move"):
    if  f_player_w:
        TAc.print(LANG.render_feedback("one-winning-move-graph", f'Starting from the node {ENV["starting_node"]} one of the possible winning moves for your graph \'{ENV["graph"]}\' is \'{gl.find_winning_move(graph, ENV["starting_node"])}\''), "yellow", ["bold"])
    else:
        move=gl.find_winning_move_on_graph_not_winning(graph,ENV['starting_node'])
        if move[0]!=(None,None):
            TAc.print(LANG.render_feedback("one-winning-move-graph", f'Starting from the node {ENV["starting_node"]} one of the possible winning moves for your graph \'{ENV["graph"]}\' is \'{move[0]}\''), "yellow", ["bold"])
        else:
            TAc.print(LANG.render_feedback("no-winning-move-graph", f'Your graph \'{ENV["graph"]}\' is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])
        
elif(info_requested=="gimme_all_winning_moves"):
    if f_player_w:
        TAc.print(LANG.render_feedback("all-winning-moves-graph", f'Starting from the node {ENV["starting_node"]} the possible winning moves for your graph \'{ENV["graph"]}\' are {gl.find_winning_moves(graph, ENV["starting_node"], True)}'), "yellow", ["bold"])
    else:
        moves=gl.find_winning_moves_on_graph_not_winning(graph,ENV['starting_node'],True)
        if moves!=[]:
            TAc.print(LANG.render_feedback("all-winning-moves-graph", f'Starting from the node {ENV["starting_node"]} the possible winning moves for your graph \'{ENV["graph"]}\' are {moves}'), "yellow", ["bold"])
        else:
            TAc.print(LANG.render_feedback("no-winning-move-graph", f'Your graph \'{ENV["graph"]}\' is a lost one. As such, I can not provide you with a winning move in this situation since no such move exists.'), "yellow", ["bold"])


exit(0)