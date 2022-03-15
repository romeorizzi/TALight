#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tabulate import tabulate
import pandas as pd
import copy
import random
import networkx as nx
import re

### CONSTANTS #########################################
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_matrix', 'with_m_and_n']
DEFAULT_FORMAT='only_matrix.txt'
#######################################################


# CONVERTERS FUNCTIONS:
def subset_to_seq(subset_sol):
    """Convert subset solution (e.g.: [[0,1],[0,0,1]]) into sequence solution (e.g.: ['r2','c3'])"""
    m = len(subset_sol[0])
    n = len(subset_sol[1])
    seq_sol = list()
    for i in range(m):
        if subset_sol[0][i]:
            seq_sol.append(f"r{i+1}")
    for j in range(n):
        if subset_sol[1][j]:
            seq_sol.append(f"c{j+1}")
    return seq_sol


def seq_to_subset(seq_sol, m, n):
    """Convert sequence solution (e.g.: ['r2','c3']) into subset solution (e.g.: [[0,1],[0,0,1]])"""
    assert isinstance(seq_sol, list)
    subset_sol = [[0]*m,[0]*n]
    for e in seq_sol:
        if e[0] == 'r':
            subset_sol[0][int(e[1:])-1] = (1-subset_sol[0][int(e[1:])-1])
        elif e[0] == 'c':
            subset_sol[1][int(e[1:])-1] = (1-subset_sol[1][int(e[1:])-1])
        else:
            raise RuntimeError(f'This seq_sol is bad written: {seq_sol}')
    return subset_sol


def parse_sol(raw_sol, sol_style, m, n):
    """Parse this raw_sol with sol_style and return the solution in correct format."""
    # Case0: general
    if len(raw_sol) > 2:
        raise RuntimeError('sol-bad-format')
    
    # Case1: sequence style
    sol = list()
    if sol_style == 'seq':
        if len(raw_sol) != 1:
            raise RuntimeError('sol-bad-format')
        # Checks no moves
        if raw_sol == ['']:
            return sol
        sol = raw_sol[0].split()
        for e in sol: 
            if any(not re.match("^((r|R|c|C)[1-9][0-9]*)$", e) for e in sol):
                raise RuntimeError('seq-regex', e)
            # Checks rows
            if (e[0] in ['r', 'R']) and (int(e[1:]) > m):
                raise RuntimeError('seq-row-m', e)
            # Checks cols
            if (e[0] in ['c', 'C']) and (int(e[1:]) > n):
                raise RuntimeError('seq-col-n', e)
        return sol
    
    # Case2: subset style
    elif sol_style == 'subset':
        # Check rows
        rows_switch = raw_sol[0].split()
        if len(rows_switch) != m:
            raise RuntimeError('subset-row-m', len(rows_switch))
        if any([not re.match(f"^(0|1)$", e) for e in rows_switch]):
            raise RuntimeError('subset-regex', raw_sol[0])
        sol.append([int(e) for e in rows_switch])
        # Check cols
        cols_switch = raw_sol[1].split()
        if len(cols_switch) != n:
            raise RuntimeError('subset-col-n', len(cols_switch))
        if any([not re.match(f"^(0|1)$", e) for e in cols_switch]):
            raise RuntimeError('subset-regex', raw_sol[1])
        sol.append([int(e) for e in cols_switch])
        return sol
    
    # Case3: invalid style
    else:
        raise RuntimeError('invalid-sol-style')


# TO STRING
def seq_to_str(seq_sol):
    """From a sequence solution (e.g.: ['r2']) returns its string form (e.g.: 'r2')"""
    return ' '.join(seq_sol)


def sol_to_str(matrix, subset_sol):
    """Print the matrix instance with the rows and cols to be switches"""
    m = len(matrix)
    n = len(matrix[0])
    sol_str = '    ' + ' '.join(str(e) for e in subset_sol[1]) + '\n'
    sol_str += f'    {"-" * (len(subset_sol[1]*2)-1)}\n'
    for i in range(m):
        sol_str += f'{subset_sol[0][i]} | '
        sol_str += ' '.join(str(e) for e in matrix[i]) + '\n'
    return sol_str[:-1]


def subset_to_str(subset_sol):
    sol = subset_to_str_list(subset_sol)
    return sol[0] + '\n' + sol[1]


def subset_to_str_list(subset_sol):
    """From a subset solution (e.g.: [[0,1],[0,0]]) returns a list with the rows string and the columns string (e.g.: ['0 1', '0 0']) or NO_SOL"""
    return [' '.join([str(e) for e in subset_sol[0]]), \
            ' '.join([str(e) for e in subset_sol[1]])]


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
    for line in lines:
        instance.append([int(e) for e in line.split()])
    return instance


def get_instance_from_dat(matrix, style=''):
    """This function returns the string representation of the given matrix instance according to the indicated format."""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    # Get lines
    lines = matrix.split('\n')
    # Parse lines
    for line in lines:
        line = line.strip() # remove whitespace before and after
        # Filter the matrix lines
        if line != '' and line[:5] != 'param' and line[:3] != 'end':
            line = line.replace(';', '') #ignore ;
            row = list()
            for e in line.split()[1:]:
                row.append(int(e))
            instance.append(row)
    return instance


# INSTANCE GENERATOR FUNCTIONS:
def gen_instance(m:int,n:int,seed:int):
    assert m >= 0
    assert n >= 0
    random.seed(seed)
    matrix=[[random.randint(0,1) for j in range(n) ] for i in range(m)]
    return matrix


def visualizza(matrix):
    index=pd.Index([str(i) for i in range(len(matrix))])
    df=pd.DataFrame(matrix,index=index)
    df = df.iloc[0:,0:]
    columns=["-"]+[str(i) for i in range(len(matrix[0])+10)]
    print(tabulate(df, headers=columns, tablefmt='fancy_grid'))
    
def conta_num_met_in(matrix):
    num_met=0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]==1:
                num_met+=1
    return num_met
        
def spara_r(matrix,r):
    num_met_destroyed=0
    for j in range(len(matrix[0])):
        if matrix[r][j]==1:
            num_met_destroyed+=1
            matrix[r][j]=0
    return num_met_destroyed

def spara_c(matrix,c):
    num_met_destroyed=0
    for i in range(len(matrix)):    
        if matrix[i][c]==1:
            num_met_destroyed+=1
            matrix[i][c]=0
    return num_met_destroyed
        
def is_feasible_shooting(m:int,n:int,matrix_original,beams,silent:bool,TAc,LANG):
    """verifyies whether a set of laser beams is enough to destroy all the asteroids. Returns either True or False. When the arg silent=False then it also prints out about its findings."""
    matrix_after_moves=copy.deepcopy(matrix_original)
    num_met_destroyed=0
    for tipo_sparo, pos_sparo in beams: 
        if tipo_sparo=='r':
            if pos_sparo < 0 or pos_sparo >= len(matrix_original):
                TAc.print(LANG.render_feedback("wrong-row", f"You shoot on the row {pos_sparo} but the row indexes go from 0 to {len(matrix_original)-1}."), "red", ["bold"])    
            num_met_destroyed+=spara_r(matrix_after_moves,pos_sparo)
        if tipo_sparo=='c':
            if pos_sparo < 0 or pos_sparo >= len(matrix_original[0]):
                TAc.print(LANG.render_feedback("wrong-col", f"You shoot on the column {pos_sparo} but the column indexes go from 0 to {len(matrix_original[0])-1}."), "red", ["bold"])
            num_met_destroyed+=spara_c(matrix_after_moves,pos_sparo)
    if conta_num_met_in(matrix_after_moves)==0:
        if not silent:
            TAc.OK()
            TAc.print(LANG.render_feedback("feasible-shooting", "Congrats. You destroyed all asteroids and saved the world!"), "green", ["bold"])
        return True
    else:
        if not silent:
            TAc.NO()
            TAc.print(LANG.render_feedback("unfeasible-shooting", "You didn't destroyed all the asteroids. See the situation after shooting your laser beams:"), "red", ["bold"])
            visualizza(matrix_after_moves)
        return False


def is_optimal_shooting(m:int,n:int,matrix,beams,silent:bool,TAc,LANG):
    """given a set of laser beams which are assumed to be enough to destroy all the asteroids, this procedure returns True if this set has minimum possible cardinality, or False otherwise. When the arg silent=False then it also prints out about its findings."""
    assert is_feasible_shooting(m,n,matrix,beams,silent=True,TAc=TAc,LANG=LANG)
    if len(beams)==opt_val(m,n,matrix):
        if not silent:
            TAc.OK()
            TAc.print(LANG.render_feedback("optimal-shooting", "You destroyed all asteroids using a minimum possible number of laser beams."), "green", ["bold"])
        return True
    else:
        if not silent:
            TAc.NO()
            TAc.print(LANG.render_feedback("feasible-but-not-optimal-shooting", "You destroyed all asteroids but you didn't use the minimum number of laser beams."), "red", ["bold"])
        return False
            
def presenza_in_rig(asteroids):
    righe=[]
    for r,c in asteroids:
        if r not in righe:
            righe.append(r)
        else:
            return True
        
def presenza_in_col(asteroids):
    col=[]
    for r,c in asteroids:
        if c not in col:
            col.append(c)
        else:
            return True        
        

def max_match(m:int,n:int,matrix):
    G = nx.Graph()
    for i in range(m):
        G.add_node(f'r{i}',label=f'r{i}')
    for j in range(n):
        G.add_node(f'c{j}',label=f'c{j}')
    
    for i in range(m):
        for j in range(n):
            if matrix[i][j]==1:
                G.add_edge(f'r{i}',f'c{j}')
    return nx.maximum_matching(G)   #return nx.max_weight_matching(G)

def max_match_bip(m:int,n:int,matrix):
    G = nx.Graph()
    G.add_nodes_from([f'r{i}' for i in range(m)], bipartite=0)
    G.add_nodes_from([f'c{j}' for j in range(n)], bipartite=1)
    G.add_edges_from([(f'r{i}',f'c{j}') for i in range(m) for j in range(n) if matrix[i][j]==1])
    return nx.bipartite.maximum_matching(G)

def min_cover(m:int,n:int,matrix):
    G = nx.Graph()
    G.add_nodes_from([str(i) for i in range(m)], bipartite=0)
    G.add_nodes_from([str(j) for j in range(n)], bipartite=1)
    G.add_edges_from([(str(i),str(j)) for i in range(m) for j in range(n) if matrix[i][j]==1])
    matching = nx.bipartite.maximum_matching(G)
    return nx.bipartite.to_vertex_cover(G, matching)

def max_independent_set(m:int,n:int,matrix):
    max_ind_set = []
    for key, value in max_match_bip(m,n,matrix).items():
        if key[0] == 'r':
            max_ind_set.append((int(key[1:]),int(value[1:])))
    return max_ind_set

def opt_val(m:int,n:int,matrix):
    return len(max_match_bip(m,n,matrix))//2

def check_row_index(index:int,m:int,TAc,LANG):
    if index < 0 or index >= m:
        TAc.print(LANG.render_feedback("row-index-out-of-range", f"Row index {index} falls outside the valid range [0,{m-1}].", {"m":m}), "red", ["bold"])
        return False
    return True
                
def check_col_index(index:int,n:int,TAc,LANG):
    if index < 0 or index >= n:
        TAc.print(LANG.render_feedback("col-index-out-of-range", f"Column index {index} falls outside the valid range [0,{n-1}].", {"n":n}), "red", ["bold"])
        return False
    return True
                
def check_is_cell_containing_asteroid(row_index:int,col_index:int,matrix,TAc,LANG):
    if not check_row_index(row_index,len(matrix),TAc,LANG):
        return False
    if not check_col_index(row_index,len(matrix[0]),TAc,LANG):
        return False
    if matrix[row_index][col_index] != 1:
        TAc.print(LANG.render_feedback("no-asteroid-cell", f"You wrote the cell ({row_index},{col_index}) but this cell contains no asteroid."), "red", ["bold"])
        return False 
    return True
                
def check_one_move_seq(move:str,m:int,n:int,TAc,LANG):
    if move.strip()=="":
        return True

    if move[0].upper()=="R":
        return check_row_index(int(move[1:]),m,TAc,LANG)
    else:
        return check_col_index(int(move[1:]),n,TAc,LANG)

def is_feasible_asteroid_set(m:int,n:int,matrix,asteroids,silent:bool,TAc,LANG):
    """verifyies whether the asteroids of a given subset are independent. Returns either True or False. When the arg silent=False then it also prints out about its findings."""
    occupied_row = [False] * m
    occupied_col = [False] * n
    for i,j in asteroids:
        if i < 0 or i >= m:
            TAc.print(LANG.render_feedback("row-index-out-of-range", f"You pointed to the cell ({i},{j}) but the row indexes go from 0 to {m-1}."), "red", ["bold"])
            return False     
        if j < 0 or j >= n:
            TAc.print(LANG.render_feedback("col-index-out-of-range", f"You pointed to the cell ({i},{j}) but the column indexes go from 0 to {n-1}."), "red", ["bold"])
            return False 
        if matrix[i][j] != 1:
            TAc.print(LANG.render_feedback("no-asteroid-cell", f"You wrote the cell ({i},{j}) but this cell contains no asteroid."), "red", ["bold"])
            return False 
        if occupied_row[i]:
            TAc.print(LANG.render_feedback("two-asteroids-on-a-same-row", f"The row r{i} contains more than one asteroid."), "red", ["bold"])
            return False
        occupied_row[i] = True
        if occupied_col[j]:
            TAc.print(LANG.render_feedback("two-asteroids-on-a-same-col", f"The column c{j} contains more than one asteroid."), "red", ["bold"])
            return False
        occupied_col[j] = True
    if not silent:
        TAc.OK()
        TAc.print(LANG.render_feedback("feasible-asteroid-set", "Congrats. Your set of asteroids is feasible."), "green", ["bold"])
    return True

    
def is_optimal_asteroid_set(m:int,n:int,matrix,asteroids,silent:bool,give_a_better_solution_if_any:bool,TAc,LANG):
    """given a subset of the cells of matrix which are assumed to contain asteroids and be independent, this procedure returns True if this set has maximum possible cardinality, or False otherwise. When the arg silent=False then it also prints out about its findings."""
    assert is_feasible_asteroid_set(m,n,matrix,asteroids,silent=True,TAc=TAc,LANG=LANG)
    if len(asteroids)==opt_val(m,n,matrix):
        if not silent:
            TAc.OK()
            TAc.print(LANG.render_feedback("optimal-asteroid-set", "Your set of independent asteroids is of maximum cardinality possible."), "green", ["bold"])
        return True
    else:
        if not silent:
            TAc.NO()
            TAc.print(LANG.render_feedback("feasible-but-not-optimal-asteroid-set", "Your asteroids are indeed independent (no two of them are on a same row or column). However, there exists a bigger set of independent asteroids."), "red", ["bold"])
        if give_a_better_solution_if_any:
            bigger_set = max_independent_set(m,n,matrix)[:len(asteroids)+1]
            TAc.print(LANG.render_feedback("bigger-asteroid-set", f"A bigger set of independent asteroids could be: {bigger_set}"), "red", ["bold"])            
        return False

# TESTS
if __name__ == "__main__":
    # CONVERTERS FUNCTIONS:
    print('Test: subset_to_seq()')
    assert subset_to_seq([[0, 0, 1], [0, 1, 0]]) == ['r3', 'c2']
    assert subset_to_seq(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: seq_to_subset()')
    assert seq_to_subset(['r3', 'c2'], 4, 4) == [[0, 0, 1, 0], [0, 1, 0, 0]]
    assert seq_to_subset(['r1', 'c2', 'c2'], 3, 3) == [[1, 0, 0], [0, 0, 0]]
    assert seq_to_subset(NO_SOL, 4, 4) == NO_SOL
    print('==> OK\n')


    print('Test: parse_sol()')
    # import math_modeling as mu
    # raw_sol = mu.get_raw_solution()
    # print(f'raw_sol: {raw_sol}')
    assert parse_sol([NO_SOL], 'seq', 2, 2) == NO_SOL
    assert parse_sol([NO_SOL], 'subset', 2, 2) == NO_SOL
    assert parse_sol(['1 0 1 0 0 ', '0 1 0 0 1 '], 'subset', 5, 5) == \
        [[1, 0, 1, 0, 0], [0, 1, 0, 0, 1]]
    assert parse_sol([''], 'seq', 2, 2) == []
    assert parse_sol(['r1 r2 c2'], 'seq', 2, 2) == ['r1', 'r2', 'c2']
    print('==> OK\n')


    # TO_STRING and FROM_STRING FUNCTIONS:
    print('Test: seq_to_str()')
    assert seq_to_str(['r3', 'c2']) == 'r3 c2'
    assert seq_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: sol_to_str()')
    assert sol_to_str([[0, 0], [1, 1]], [[0, 1], [0, 0]]) == \
        "    0 0\n" + \
        "    ---\n" + \
        "0 | 0 0\n" + \
        "1 | 1 1"
    assert sol_to_str([[0, 0], [0, 1]], NO_SOL) == \
        "    ? ?\n" + \
        "    ---\n" + \
        "? | 0 0\n" + \
        "? | 0 1"
    print('==> OK\n')


    print('Test: subset_to_str()')
    assert subset_to_str([[0, 0, 1], [0, 1, 0]]) == "0 0 1\n0 1 0"
    assert subset_to_str(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: subset_to_str_list()')
    assert subset_to_str_list([[0, 0, 1], [0, 1, 0]]) == ['0 0 1', '0 1 0']
    assert subset_to_str_list(NO_SOL) == NO_SOL
    print('==> OK\n')


    print('Test: instance_to_str()')
    assert instance_to_str([[0, 0], [1, 1]]) == '0 0\n1 1'
    print('==> OK\n')


    print('Test: instance_to_txt()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: instance_to_dat()')
    print('MAYBE TODO?')
    print('==> OK\n')


    print('Test: get_instance_from_str()')
    print('==> OK\n')


    print('Test: get_instance_from_txt()')
    assert get_instance_from_txt('0 0\n1 1', 'only_matrix') == [[0, 0], [1, 1]]
    print('==> OK\n')


    print('Test: get_instance_from_dat()')
    dat_instance = \
        "param M := 10;  # Number of rows\n" + \
        "param N := 2;  # Number of columns\n" + \
        "param MATRIX :  1 2 3 4 5 6 7 8 9 10:=\n" + \
        "                        \n" + \
        "              1    1 0 1 1 0 1 0 0 0 1   \n" + \
        "                                            \n" + \
        "\n" + \
        "              2    0 1 0 0 1 0 0 1 1 1 ;\n" + \
        "end;\n"
    assert get_instance_from_dat(dat_instance)  == [[1, 0, 1, 1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 1, 0, 0, 1, 1, 1]]
    dat_instance = \
        "param M := 2;  # Number of rows\n" + \
        "param N := 2;  # Number of columns\n" + \
        "param MATRIX :  1 2:=\n" + \
        "                        \n" + \
        "              1    1 0   \n" + \
        "                                            \n" + \
        "\n" + \
        "              2    0 1;\n" + \
        "end;\n"
    assert get_instance_from_dat(dat_instance)  == [[1, 0], [0, 1]]
    print('==> OK\n')


    # INSTANCE GENERATOR FUNCTIONS:
    print('Test: is_solvable_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_instance_seed()')
    print('FOR DEFINITION')
    print('==> OK\n')


    print('Test: gen_instance()')
    print('MAYBE TODO?')
    print('==> OK\n')


    # CORE FUNCTIONS:
    print('Test: is_feasible_shooting()')
    print('Test: is_optimal_shooting()')

    print("FINISH")


