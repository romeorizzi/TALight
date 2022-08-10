#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt

def player_flip(n_player):
    if n_player==1:
        n_player=2
    else:
        n_player=1
    return n_player

def is_edge(graph,u,v):
    try:
        return nx.is_path(graph,[u,v])
    except KeyError:
        return False

def generate_random_graph(nodes):
    return nx.fast_gnp_random_graph(nodes,.5)

def add_edge(graph, start, end):
    return graph.add_edge(start, end)

def get_edges(graph):
    return nx.edges(graph)

def get_edges_from_input_str(str_in):
    list_edges=list(str_in.split(')('))
    list_edges[0]=list_edges[0][1:]
    list_edges[-1]=list_edges[-1][:-1]
    return list_edges

def get_str_edges_from_printed_str(str_in):
    str_in=str_in[1:-1]
    str_out=''
    list_edges=list(str_in.split('), ('))
    list_edges[0]=list_edges[0][1:]
    list_edges[-1]=list_edges[-1][:-1]
    for edge in list_edges:
        u,v=edge.split(', ')
        str_out=str_out+'('+u+' '+v+')'
    return str_out

def generate_graph_from_input(str_in):
    graph=nx.empty_graph(1)
    list_edges=get_edges_from_input_str(str_in)
    for edge in list_edges:
        u,v=edge.split(' ')
        u=int(u)
        v=int(v)
        add_edge(graph, u,v)
    return graph

def get_nodes(graph):
    g_nodes=[]
    for node in nx.nodes(graph):
        g_nodes.append(node)
    return sorted(g_nodes)

def get_nodes_from_edges(edges):
    e_nodes=[]
    for edge in edges:
        u,v=edge
        e_nodes.append(u)
        e_nodes.append(v)
    e_nodes=list(set(e_nodes))
    return sorted(e_nodes)

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    for node in nx.all_neighbors(graph,start):
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
  
# function to generate all possible paths
def find_all_paths(graph, start, end, path =[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in nx.all_neighbors(graph,start):
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_shortest_path(graph, start, end):
    return nx.shortest_path(graph, start, end)

def find_matching(edges):
    matching = set()
    nodes = set()
    for edge in edges:
        # If the edge isn't covered, add it to the matching
        # then remove neighborhood of u and v from consideration.
        u, v = edge
        if u not in nodes and v not in nodes and u != v:
            matching.add(edge)
            nodes.update(edge)
    return list(matching)

def find_perfect_matching(graph):
    if len(graph)%2!=0:
        return []
    edges=get_edges(graph)
    edges=list(edges)
    matching=find_matching(edges)
    if len(matching)==len(graph)//2:
        return matching
    first_edge=edges.pop(0)
    edges.append(first_edge)
    while edges[0]!=first_edge:
        matching=find_matching(edges)
        if len(matching)==len(graph)//2:
            return matching
        edges.append(edges.pop(0))
    return []
        
def first_player_win(graph):
    return find_perfect_matching(graph)!=[]

def format_path(path):
    if path==None:
        return
    f_path=''
    for node in path:
        if f_path=='':
            f_path=f_path+str(node)
        else:
            f_path=f_path+'->'+str(node)
    return [f_path]  

def format_paths(paths):
    if paths==[]:
        return None
    list_paths=[]
    for path in paths:
        f_path=''
        for node in path:
            if f_path=='':
                f_path=f_path+str(node)
            else:
                f_path=f_path+'->'+str(node)
        list_paths.append(f_path)
    return list_paths

def print_graph(graph):
    nx.draw_networkx(graph)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

def get_subgraphs(graph):
    subs=[]
    for sub in nx.connected_components(graph):
        subs.append(nx.subgraph(graph,sub))
    return subs

def find_winning_move(graph,node):
    matching=find_perfect_matching(graph)
    edges=get_edges(graph)
    moves=list(set(edges).intersection(matching))
    for move in moves:
        u,v=move
        if u==node:
            return (node,v)
        if v==node:
            return (node,u)

def find_winning_moves(graph,node,rmv_dup=False):
    matching=find_perfect_matching(graph)
    edges=get_edges(graph)
    moves=list(set(edges).intersection(matching))
    win_moves=[]
    for move in moves:
        u,v=move
        if u==node:
            win_moves.append((node,v))
        if v==node:
            win_moves.append((node,u))
    if rmv_dup:
        win_moves=list(dict.fromkeys(win_moves))
    return win_moves

def find_winning_move_on_graph_not_winning(graph,node):
    nodes=get_nodes(graph)
    nodes.remove(node)
    subgraphs=get_subgraphs(nx.subgraph(graph,nodes))
    for sub in subgraphs:
        if not(first_player_win(sub)):
            edges=get_edges(graph)
            nodes=get_nodes(sub)
            for edge in edges:
                u,v=edge
                if u==node and v in nodes:
                    return (node,v),nodes
                if v==node and u in nodes:
                    return (node,u),nodes
    return (None,None),nodes

def find_move(graph,node):
    (u,v),nodes=find_winning_move_on_graph_not_winning(graph,node)
    if u!=None and v!=None:
        return (u,v),nodes
    edges=get_edges(graph)
    for edge in edges:
        u,v=edge
        if u==node:
            return (node,v),nodes
        if v==node:
            return (node,u),nodes

def find_winning_moves_on_graph_not_winning(graph,node,rmv_dup=False):
    nodes=get_nodes(graph)
    nodes.remove(node)
    subgraphs=get_subgraphs(nx.subgraph(graph,nodes))
    moves=[]
    for sub in subgraphs:
        if not(first_player_win(sub)):
            edges=get_edges(graph)
            nodes=get_nodes(sub)
            for edge in edges:
                u,v=edge
                if u==node and v in nodes:
                    moves.append((node,v))
                if v==node and u in nodes:
                    moves.append((node,u))
    if rmv_dup:
        moves=list(dict.fromkeys(moves))
    return moves

def cut_graph(graph, node):
    subgraphs=get_subgraphs(graph)
    for sub in subgraphs:
        sub_nodes=get_nodes(sub)
        if node in sub_nodes:
            return sub

def update_graph(graph,node):
    nodes=get_nodes(graph)
    nodes.remove(node)
    return nx.subgraph(graph,nodes)

def computer_move(graph, node):
    graph=cut_graph(graph,node)
    if first_player_win(graph):
        nodes=get_nodes(graph)
        nodes.remove(node)
        return find_winning_move(graph,node),nx.subgraph(graph,nodes)
    else:
        (u,v),nodes=find_move(graph,node)
        return (u,v),nx.subgraph(graph,nodes)

# TESTS
if __name__ == "__main__":
    graph=nx.empty_graph(0)
    add_edge(graph,0,1)
    add_edge(graph,1,2)
    add_edge(graph,0,3)
    add_edge(graph,3,4)
    add_edge(graph,2,5)
    print('Test: first_player_win(graph)')
    assert first_player_win(graph)
    print('==> OK')