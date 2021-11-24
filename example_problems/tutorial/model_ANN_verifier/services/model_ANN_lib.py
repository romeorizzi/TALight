#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from tabulate import tabulate
import pandas as pd
import copy
import random
import re
#import networkx as nx

### CONSTANTS #########################################
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_values','values_with_info']
DEFAULT_FORMAT='only_values.txt'
#######################################################

# INSTANCE GENERATOR FUNCTIONS:
def gen_instance(n_nodes,seed:int):
    assert len(n_nodes) >= 2 

    random.seed(seed)
    ann =[]

    # first append the total number of layers
    ann.append(len(n_nodes))

    # then we append the number of nodes for each layer
    ann.append(n_nodes)

    # then we generate n_nodes_i * n_nodes_i+1 weights
    for i in range(1,len(n_nodes)):
        weights = [random.randint(-10,10) for _ in range(n_nodes[i-1]*n_nodes[i])] 
        ann.append(weights)

    return ann


def instance_to_str(instance):
    instance_str = str(instance[0]) + '\n'
    instance_str += ' '.join(str(e) for e in instance[1]) + '\n'

    for i in range(2,len(instance)):
        instance_str += ' '.join(str(e) for e in instance[i]) + '\n'

    return instance_str


def instance_to_txt(instance, style='only_values'):
    """This function returns the string representation of the given matrix instance according to the indicated style"""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance_str = 'Tot_layers: ' + str(instance[0]) + '\n' if style=='values_with_info' else str(instance[0]) + '\n'
    instance_str += 'Tot_Nodes: ' + ' '.join(str(e) for e in instance[1]) + '\n' if style=='values_with_info' else ' '.join(str(e) for e in instance[1]) + '\n'
    
    if style=='values_with_info':
        instance_str += 'ANN_weigths: \n' 

    for i in range(2,len(instance)):
        instance_str += ' '.join(str(e) for e in instance[i]) + '\n'

    return instance_str

#print(instance_to_txt([3, [3, 4, 1], [1,2,3,4,5,6,7,8,9,10,11,12], [1,2,3,4]],'values_with_info'))

def instance_to_dat(instance, style=''):
    """This function returns the dat representation of the given matrix instance according to the indicated style"""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    TOT_LAYERS = str(instance[0])
    N_NODES = ' '.join(str(e) for e in instance[1])

    output = f"param TOT_LAYERS := {TOT_LAYERS};  # Total Number of layers in the ANN\n"
    output += f"param N_NODES := {N_NODES};  # Number of nodes for each layer\n"
    output += "param ANN_WEIGTHS :=\n"

    for i in range(2,len(instance)):
        output += f"                     {i-1}   "
        output += ' '.join(str(e) for e in instance[i])
        output += " ;\n" if i == (len(instance) - 1) else "\n"
        
    output += "end;"
    return output

#print(instance_to_dat([3, [3, 4, 1], [1,2,3,4,5,6,7,8,9,10,11,12], [1,2,3,4]],''))

def instance_to_str(instance, format='default'):
    """This function returns the string representation of the given ANN instance according to the indicated format"""
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
        return instance_to_dat(instance, format_secondary)
    if format_primary == 'txt':
        return instance_to_txt(instance, format_secondary)