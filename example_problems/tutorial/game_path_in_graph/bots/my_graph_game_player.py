#!/usr/bin/env python3
from bot_lib import Bot

import graph_game_lib as gl

BOT = Bot(report_inputs=False,reprint_outputs=False)

while True:
    line = BOT.input()
    cur_graph,start_node = map(str,line.split('] '))
    start_node=int(start_node)
    cur_graph=cur_graph+']'
    edges=gl.get_str_edges_from_printed_str(cur_graph)
    graph=gl.generate_graph_from_input(edges)
    (u,v),graph=gl.computer_move(graph,start_node)
    print(f"{u} {v}")
