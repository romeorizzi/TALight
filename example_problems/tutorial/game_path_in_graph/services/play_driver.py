#!/usr/bin/env python3

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import random
import graph_game_lib as gl

# METADATA OF THIS TAL_SERVICE:
problem="graph_game"
service="play"

args_list = [
    ('graph',str),
    ('starting_node',int),
    ('TALight_first_to_move',int),
    ('watch',str),
    ('seed',int),
    ('opponent',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:

def close_service_and_print_term_signal_for_bots():
    TAc.Finished(only_term_signal=True)
    exit(0)

if ENV['seed']>0:
    random.seed(ENV['seed'])
    nodes=int(round((random.random())*10,0))
    if nodes==0 or nodes==1:
        nodes=10
    graph=gl.generate_random_graph(nodes)
    nodes=gl.get_nodes(graph)
    start_node=random.choice(nodes)
else:
    graph=gl.generate_graph_from_input(ENV['graph'])
    start_node=ENV['starting_node']

if not(start_node in gl.get_nodes(graph)):
    TAc.print(LANG.render_feedback("graph-illegal-start-node", '# We have a problem. The starting node is not valid because is not a node of the graph.'), "red", ["bold"])
    exit(0)
u=start_node
graph=gl.cut_graph(graph,start_node)

def I_have_lost():
    if ENV['opponent'] == 'computer':
        TAc.print(LANG.render_feedback("graph-TALight_lost", f'# It is my turn to move, on a node of the graph without edges with untouched nodes. Since this configuration admits no valid move, then I have lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("graph-you-won", f'# You won!'), "green", ["bold"])
    else:
        TAc.print(LANG.render_feedback("graph-player-lost-msg", f'# It is the turn of player {gl.player_flip(n_player)} to move, on a node of the graph without edges with untouched nodes. Since this configuration admits no valid move, then player {gl.player_flip(n_player)} has lost this match.'), "yellow", ["bold"])
        TAc.print(LANG.render_feedback("graph-player-won", f'# Player {n_player} won!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()
    
def you_have_lost():
    TAc.print(LANG.render_feedback("graph-you-have-lost", f'# It is your turn to move, on a node of the graph without edges with untouched nodes. Since this configuration admits no valid move, then you have lost this match.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("graph-you-lost", f'# You lost!'), "green", ["bold"])
    close_service_and_print_term_signal_for_bots()

I_AM = LANG.render_feedback("I-am", 'I am')
YOU_ARE = LANG.render_feedback("you-are", 'you are')
TALIGHT_IS = LANG.render_feedback("TALight-is", 'TALight is')
PLAYER_1_IS = LANG.render_feedback("Player-1-is", 'Player 1 is')
PLAYER_2_IS = LANG.render_feedback("Player-2-is", 'Player 2 is')
def watch(graph,start_node, first_to_move, second_to_move):
    assert first_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS] 
    assert second_to_move in [I_AM,YOU_ARE,TALIGHT_IS,PLAYER_1_IS,PLAYER_2_IS]
    if ENV["watch"] == 'no_watch':
        return
    TAc.print(f'# watch={ENV["watch"]}: ', "blue", end='')
    f_player_w = gl.first_player_win(graph)
    win_moves=[]
    if not(f_player_w):
        win_moves=gl.find_winning_moves_on_graph_not_winning(graph,start_node,True)
    #win_moves.extend(gl.find_winning_moves(graph,start_node,True))
    else:
        win_moves=gl.find_winning_moves(graph,start_node,True)
    win_moves=list(dict.fromkeys(win_moves))
    if ENV["watch"] == 'watch_winner':
        if not(f_player_w) and win_moves==[]:
            TAc.print(LANG.render_feedback("graph-watch-winner-who-moves-loses", f'{second_to_move} ahead, since \'{gl.get_edges(graph)}\' is a who-moves-loses configuration.'), "blue")
        else:
            TAc.print(LANG.render_feedback("graph-watch-winner-who-moves-wins", f'{first_to_move} ahead, since \'{gl.get_edges(graph)}\' is a who-moves-wins configuration.'), "blue")
    elif ENV['watch'] == 'num_winning_moves' :
        #win_moves = gl.find_moves_graph_game(graph)
        if len(win_moves) > 0:
            TAc.print(LANG.render_feedback("graph-num-winning-moves-n", f'the current graph \'{gl.get_edges(graph)}\' admits {len(win_moves)} winning moves'), "blue")
        else:
            TAc.print(LANG.render_feedback("graph-num-winning-moves-0", f'the current graph \'{gl.get_edges(graph)}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'list_winning_moves':
        #win_moves = gl.find_moves_graph_game(graph, True)
        if len(win_moves) > 1:
            TAc.print(LANG.render_feedback("graph-list-multiple-winning-moves", f'for the current graph \'{gl.get_edges(graph)}\' the winning moves are {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result graph is the same', "blue")
        elif len(win_moves) == 1:
            TAc.print(LANG.render_feedback("graph-list-one-winning-move", f'for the current graph \'{gl.get_edges(graph)}\' the winning move is {win_moves}'), "blue")
            TAc.print('# The duplicates are removed, if the result graph is the same', "blue")
        else:
            TAc.print(LANG.render_feedback("graph-list-none-winning-moves", f'the current graph \'{gl.get_edges(graph)}\' admits no winning move'), "blue")
    elif ENV['watch'] == 'print_current_graph':
        TAc.print(LANG.render_feedback("graph-print-current-graph", f'the current graph with the available nodes is printed'), "blue")
        gl.print_graph(graph)



if ENV["TALight_first_to_move"] == 1 and ENV['opponent'] == 'computer': # if the user plays the match as second to move
    if len(graph)==1: # no valid moves on the graph ''. TALight first to move loses the match
        I_have_lost()
    
    watch(graph,start_node, first_to_move=I_AM, second_to_move=YOU_ARE)
        
    # TALight makes its move updating the new graph:
    (new_u,new_v),new_graph=gl.computer_move(graph,start_node)
    TAc.print(LANG.render_feedback("graph-server-move", f'# My move is from node {new_u} to node {new_v}.'), "green", ["bold"])
    #graph=new_graph
    u=new_u
    v=new_v
    start_node=new_v
    graph=gl.cut_graph(new_graph,start_node)

n_player=1

while True:
    if len(graph)==1: # the graph '' admits no valid move. The turn is to the user who has no move available and loses the match. TALight wins.
        you_have_lost()
    if ENV['opponent'] == 'computer':
        watch(graph,start_node, first_to_move=YOU_ARE, second_to_move=I_AM)
    else:
        if n_player==1:
            watch(graph,start_node, first_to_move=PLAYER_1_IS, second_to_move=PLAYER_2_IS)
        else:
            watch(graph,start_node, first_to_move=PLAYER_2_IS, second_to_move=PLAYER_1_IS)
    if ENV['opponent'] == 'computer':  
        TAc.print(LANG.render_feedback("graph-your-turn", f'# It is your turn to move on the graph \'{gl.get_edges(graph)}\' starting from node {start_node} to a new node. The edge must be an edge of the current graph.'), "yellow", ["bold"])
    else:
        TAc.print(LANG.render_feedback("graph-player-turn", f'# It is the turn of player {n_player} to move from graph \'{gl.get_edges(graph)}\' starting from node {start_node} to a new node. The edge must be an edge of the current graph.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("graph-user-move", f'# Please, insert your move just underneath the current graph and the starting node as reported here: '), "yellow", ["bold"])

    TAc.print(LANG.render_feedback("graph-prompt", f'{gl.get_edges(graph)} {start_node}'), "yellow", ["bold"])
    new_u, new_v = TALinput(int, 2, TAc=TAc)
    
    if new_u!=start_node:
        TAc.print(LANG.render_feedback("graph-illegal-move", '# We have a problem. Your move is not valid. The starting node on your move is not the right one.'), "red", ["bold"])
        exit(0)
    if new_u==new_v:
        TAc.print(LANG.render_feedback("graph-illegal-move", '# We have a problem. Your move is not valid. You can\'t move to the same node'), "red", ["bold"])
        exit(0)
    if not gl.is_edge(graph, new_u,new_v):
        TAc.print(LANG.render_feedback("graph-illegal-move", '# We have a problem. Your move is not valid.'), "red", ["bold"])
        exit(0)

    new_graph=gl.update_graph(graph,start_node)
    new_graph=gl.cut_graph(new_graph,new_v)
    start_node=new_v

    if len(new_graph)==1: # TALight has no valid move available and loses the match. The user wins.
        I_have_lost()

    if ENV['opponent'] == 'computer':
        watch(new_graph,start_node, first_to_move=I_AM, second_to_move=YOU_ARE)
        (u,v),graph=gl.computer_move(new_graph,start_node) # TALight makes its move
        start_node=v
        graph=gl.cut_graph(graph,start_node)
        TAc.print(LANG.render_feedback("graph-server-move", f'# My move is from node {u} to node {v}.'), "green", ["bold"])
    else:
        n_player=gl.player_flip(n_player)
        graph=new_graph
        u=new_u
        v=new_v
        start_node=new_v