#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:34:12 2021

@author: Aurora Rossi

"""

from tabulate import tabulate
import pandas as pd
import copy
import random
import networkx as nx

### CONSTANTS #########################################
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_matrix', 'with_m_and_n']
DEFAULT_FORMAT='only_matrix.txt'
#######################################################


# CONVERTERS FUNCTIONS:
def instance_to_str(matrix, format='default'):
    """This function returns the string representation of the given matrix instance according to the indicated format"""
    # Get default
    format = DEFAULT_FORMAT if format=='default' else format
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get matrix in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return instance_to_dat(matrix, format_secondary)
    if format_primary == 'txt':
        return instance_to_txt(matrix, format_secondary)

def instance_to_txt(matrix, style='only_matrix'):
    """This function returns the string representation of the given matrix instance according to the indicated style"""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    output = ""
    if style == "with_m_and_n":
        output = f"{len(matrix)} {len(matrix[0])}\n"
    output += '\n'.join((''.join(str(col) for col in row) for row in matrix))
    return output


def instance_to_dat(matrix, style=''):
    """This function returns the dat representation of the given matrix instance according to the indicated style"""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    M = len(matrix)
    N = len(matrix[0])
    output = f"param M := {M};  # Number of rows\n"
    output += f"param N := {N};  # Number of columns\n"
    output += "param MATRIX :  " + " ".join([str(i) for i in range(1,N+1)]) + " :=\n"
    for i in range(M):
        output += f"            {i+1}   "
        output += ' '.join(str(col) for col in matrix[i])
        output += ";\n" if i == (M - 1) else "\n"
    output += "end;"
    return output


# FROM STRING
def get_instance_from_str(matrix, format):
    """This function returns the string representation of the given matrix instance according to the indicated format."""
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get matrix in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return get_instance_from_dat(matrix, format_secondary)
    if format_primary == 'txt':
        return get_instance_from_txt(matrix, format_secondary)


def get_instance_from_txt(matrix, style='only_matrix'):
    """This function returns the string representation of the given matrix instance according to the indicated format."""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    lines = matrix.split('\n')
    if format == "with_m_and_n":
        lines = lines[2:]
    for l in lines:
        instance.append([int(e) for e in l.split()])
    return instance


def get_instance_from_dat(matrix, style=''):
    """This function returns the string representation of the given matrix instance according to the indicated format."""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    # Get lines
    lines = matrix.split('\n')
    # Parse lines
    for l in lines:
        l = l.strip() # remove whitespace before and after
        # Filter the matrix lines
        if l != '' and l[:5] != 'param' and l[:3] != 'end':
            l = l.replace(';', '') #ignore ;
            row = list()
            for e in l.split()[1:]:
                row.append(int(e))
            instance.append(row)
    return instance


# INSTANCE GENERATOR FUNCTIONS:
def gen_instance(m,n,seed:int):
    assert m >= 0
    assert n >= 0
    if seed==0:
        random.seed()
        seed = random.randint(100000,999999)
    random.seed(seed)
    quad=[[random.randint(0,1) for j in range(n) ] for i in range(m)]
    return quad,seed


def visualizza(matrix):
    index=pd.Index([str(i) for i in range(len(matrix))])
    df=pd.DataFrame(matrix,index=index)
    df = df.iloc[0:,0:]
    columns=["-"]+[str(i) for i in range(len(matrix[0])+10)]
    print(tabulate(df, headers=columns, tablefmt='fancy_grid'))
    
        

def conta_num_met_in(quad):
    num_met=0
    for i in range(len(quad)):
        for j in range(len(quad[0])):
            if quad[i][j]=='*':
                num_met+=1
    return num_met
        
def spara_r(quad,r):
    num_met_destroyed=0
    for j in range(len(quad[0])):
        if quad[r][j]=='*':
            num_met_destroyed+=1
            quad[r][j]='.'
    return num_met_destroyed

def spara_c(quad,c):
    num_met_destroyed=0
    for i in range(len(quad)):    
        if quad[i][c]=='*':
            num_met_destroyed+=1
            quad[i][c]='.'
    return num_met_destroyed
        
def verifica(raggi,quadro_istanza_originale,TAc,LANG):
    quadro_scratch=copy.deepcopy(quadro_istanza_originale)
    num_met_destroyed=0
    num_co=max_match(quadro_istanza_originale)
    for tipo_sparo, pos_sparo in raggi:
        
        if tipo_sparo=='r':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale):
                TAc.print(LANG.render_feedback("wrong-row", f"You shoot on the row {pos_sparo} but the row indexes go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])

    
            num_met_destroyed+=spara_r(quadro_scratch,pos_sparo)
        if tipo_sparo=='c':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale[0]):
                TAc.print(LANG.render_feedback("wrong-col", f"You shoot on the column {pos_sparo} but the column indexes go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            num_met_destroyed+=spara_c(quadro_scratch,pos_sparo)
    if conta_num_met_in(quadro_scratch)==0 and len(raggi)==num_co:
        TAc.OK()
        TAc.print(LANG.render_feedback("correct", "You destroyed all asteroids with minimum number of laser beams."), "green", ["bold"])
    elif conta_num_met_in(quadro_scratch)==0 and len(raggi)>num_co:
        TAc.NO()
        TAc.print(LANG.render_feedback("semi-correct", "You destroyed all asteroids but you didn't use the minimum number of laser beams."), "red", ["bold"])
    else:
        TAc.NO()
        TAc.print(LANG.render_feedback("wrong", "You didn't destroyed all asteroids, see what happens:"), "red", ["bold"])
        visualizza(quadro_scratch)

            
def presenza_in_rig(asteroidi):
    righe=[]
    for r,c in asteroidi:
        if r not in righe:
            righe.append(r)
        else:
            return True
        
def presenza_in_col(asteroidi):
    col=[]
    for r,c in asteroidi:
        if c not in col:
            col.append(c)
        else:
            return True        
        

def max_match(quad):
    G = nx.Graph()
    for i in range(len(quad)):
        G.add_node(f'r{i}',label=f'r{i}')
    for j in range(len(quad[0])):
        G.add_node(f'c{j}',label=f'c{j}')
    
    
    for i in range(len(quad)):
        for j in range(len(quad[0])):
            if quad[i][j]=='*':
                G.add_edge(f'r{i}',f'c{j}')
    return len(nx.max_weight_matching(G))

                
def verifica_asteroidi_indipendenti(asteroidi,quadro_istanza_originale,TAc,LANG):
    num_co=max_match(quadro_istanza_originale)
    for i,j in asteroidi:
        if i < 0 or i >= len(quadro_istanza_originale):
            TAc.print(LANG.render_feedback("wrong-row", f"You shoot on the cell ({i},{j}) but the right row indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            return
            
            
        if j < 0 or j >= len(quadro_istanza_originale[0]):
            TAc.print(LANG.render_feedback("wrong-col", f"You shoot on the cell ({i},{j}) but the right column indeces go from 0 to {len(quadro_istanza_originale)}."), "red", ["bold"])
            return 
        if quadro_istanza_originale[i][j]!='*':
            TAc.print(LANG.render_feedback("wrong-cell", f"You wrote the cell ({i},{j}) but it doesn't contain asteroids."), "red", ["bold"])
            return 
    if presenza_in_rig(asteroidi):
        TAc.print(LANG.render_feedback("wrong-row2", f"You insert al least two cell of the same row {i}.You can not take more than one cell per row."), "red", ["bold"])
        return 
        
    if presenza_in_col(asteroidi):
        TAc.print(LANG.render_feedback("wrong-col2", f"You insert al least two cell of the same column {j}.You can not take more than one cell per column."), "red", ["bold"])
        return 
    if len(asteroidi)==num_co:
        return TAc.OK(),TAc.print(LANG.render_feedback("right", "Your set is feaseble and maximum."), "green", ["bold"])    
    if len(asteroidi)<num_co:
        return TAc.NO(),TAc.print(LANG.render_feedback("wrong_set", "Your set is feaseble but not maximum."), "red", ["bold"])    
    



