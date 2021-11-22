#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from tabulate import tabulate
import pandas as pd
import copy
import random
import re
import networkx as nx


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