#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import itertools

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

def find_perfect_matchings(graph,rmv_dup=False):
    if len(graph)%2!=0:
        return []
    edges=get_edges(graph)
    edges=list(edges)
    matching=find_matching(edges)
    p_matchings=[]
    if len(matching)==len(graph)//2:
        p_matchings.append(matching)
    first_edge=edges.pop(0)
    edges.append(first_edge)
    while edges[0]!=first_edge:
        matching=find_matching(edges)
        if len(matching)==len(graph)//2:
            p_matchings.append(matching)
        edges.append(edges.pop(0))
    if rmv_dup:
        p_matchings.sort()
        p_matchings=list(k for k,_ in itertools.groupby(p_matchings))
    return p_matchings
        
def first_player_win(graph):
    return find_perfect_matching(graph)!=[]

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
    matchings=find_perfect_matchings(graph)
    win_moves=[]
    for matching in matchings:
        edges=get_edges(graph)
        moves=list(set(edges).intersection(matching))
        for move in moves:
            u,v=move
            if u==node:
                win_moves.append((node,v))
            if v==node:
                win_moves.append((node,u))
    if rmv_dup:
        win_moves=list(dict.fromkeys(win_moves))
    return win_moves

def find_winning_move_on_graph_not_winning(graph,node):#,search=False):
    neighbors=nx.neighbors(graph,node)
    nodes=get_nodes(graph)
    nodes.remove(node)
    graph=nx.subgraph(graph,nodes)
    f_player_w=True
    for neighbor in neighbors:
        subgraph=cut_graph(graph,neighbor)
        edges=nx.edges(subgraph,neighbor)
        subnodes=get_nodes(subgraph)
        subnodes.remove(neighbor)
        subgraphs=get_subgraphs(nx.subgraph(subgraph,subnodes))
        indexes=[]
        for index,sub in enumerate(subgraphs):
            if not(first_player_win(sub)):#==search:
                f_player_w=False
                indexes.append(index)
        if f_player_w:
            return(node,neighbor),nodes
        else:
            for index in indexes:
                there_are_moves=inspect_subgraph(subgraphs[index],neighbor,edges)#,not(search))
            if there_are_moves:
                return (node,neighbor),nodes
    return (None,None),nodes

def inspect_subgraph(graph,node,edges,search=True):
    if len(graph)==1:
        return not(search)
    if len(graph)==2:
        return search
    graph=nx.Graph(graph)
    for edge in edges:
        u,v=edge
        if (u==node and v in get_nodes(graph)) or (v==node and u in get_nodes(graph)):
            add_edge(graph,u,v)
    neighbors=nx.neighbors(graph,node)
    nodes=get_nodes(graph)
    nodes.remove(node)
    graph=nx.subgraph(graph,nodes)
    f_player_w=True
    response_values=[]
    for neighbor in neighbors:
        #f_player_w=True
        #response_values=[]
        subgraph=cut_graph(graph,neighbor)
        subedges=nx.edges(subgraph,neighbor)
        subnodes=get_nodes(subgraph)
        subnodes.remove(neighbor)
        subgraphs=get_subgraphs(nx.subgraph(subgraph,subnodes))
        indexes=[]
        for index,sub in enumerate(subgraphs):
            if first_player_win(sub)==search:
                f_player_w=False
                indexes.append(index)
        if f_player_w:
            #return True
            response_values.append(True)
        else:
            for index in indexes:
                there_are_moves=inspect_subgraph(subgraphs[index],neighbor,subedges,not(search))
                response_values.append(there_are_moves)
    return all(response_values)
        

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

def find_winning_moves_on_graph_not_winning(graph,node,rmv_dup=False,search=False):
    neighbors=nx.neighbors(graph,node)
    nodes=get_nodes(graph)
    nodes.remove(node)
    graph=nx.subgraph(graph,nodes)
    f_player_w=True
    moves=[]
    for neighbor in neighbors:
        subgraph=cut_graph(graph,neighbor)
        edges=nx.edges(subgraph,neighbor)
        subnodes=get_nodes(subgraph)
        subnodes.remove(neighbor)
        subgraphs=get_subgraphs(nx.subgraph(subgraph,subnodes))
        indexes=[]
        for index,sub in enumerate(subgraphs):
            if not(first_player_win(sub)):#==search:
                f_player_w=False
                indexes.append(index)
        if f_player_w:
            moves.append((node,neighbor))
        else:
            for index in indexes:
                there_are_moves=inspect_subgraph(subgraphs[index],neighbor,edges)#,not(search))
            if there_are_moves:
                moves.append((node,neighbor))
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
