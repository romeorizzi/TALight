#!/usr/bin/env python3
from sys import stderr, exit, stdin

from multilanguage import Env, Lang, TALcolors
from TALinputs import *

import model_ANN_lib as annl
import random
from math_modeling import ModellingProblemHelper, get_problem_path_from


# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_spec',str),
    ('instance_id',int),
    ('n_nodes',str),
    ('seed',int),
    ('input_values',str),
    ('activation',str),
    ('watch_layers',str),
    ('decimal_digits', int)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:
format = 'plain.txt'

# ====================== get the instance ==========================================
if ENV['instance_spec'] == 'catalogue1':
    # Initialize ModellingProblemHelper
    mph = ModellingProblemHelper(TAc, get_problem_path_from(__file__))
    # Get dat file
    instance_str = mph.get_file_str_from_id(ENV['instance_id'], format)
    instance = annl.get_instance_from_str(instance_str, format)

elif ENV['instance_spec'] == 'random':
    # Get instance
    assert ENV['instance_spec'] == 'random'
    instance = annl.gen_instance(ENV['n_nodes'], ENV['seed'])

else:
    TAc.print(LANG.render_feedback("user_instance", 'Insert your instance: '), "yellow", ["bold"]) 
    instance_str = ''
   
    while True:
        input = TALinput(str, TAc=TAc, LANG=LANG)
        if 'end' in input:
            break

        instance_str += ' '.join(str(e) for e in input) 
        instance_str += '\n'
        
    instance = annl.get_instance_from_str(instance_str,format)
  
if ENV['instance_spec'] == 'catalogue1':
    TAc.print(LANG.render_feedback("instance", f'The instance on which the server will perform the forward propagation is:\n{" ".join(str(x) for x in instance[1])}, instance_id = {ENV["instance_id"]}'), "yellow", ["bold"]) 
elif ENV['instance_spec'] == 'terminal':
    TAc.print(LANG.render_feedback("instance", f'The instance on which the server will perform the forward propagation is:\n{" ".join(str(x) for x in instance[1])}'), "yellow", ["bold"]) 
else:
    TAc.print(LANG.render_feedback("instance", f'The instance on which the server will perform the forward propagation is:\n{" ".join(str(x) for x in instance[1])}, seed = {ENV["seed"]}'), "yellow", ["bold"]) 


# ====================== get the input values or generate them ==========================================
n_nodes_input_layer = instance[1][0]

if ENV['input_values'] == 'random':
    values_input_layer = [random.randint(-10,10) for _ in range(n_nodes_input_layer)]
else:
    values_input_layer = ENV['input_values'].split(' ')
    values_input_layer = list(map(float, values_input_layer))
    values_input_layer = [round(v, ENV['decimal_digits']) for v in values_input_layer]

    if len(values_input_layer) < instance[1][0]:
        TAc.print(LANG.render_feedback("error", f'The input layer has {instance[1][0]} nodes but you provided only {len(values_input_layer)} values. Check your input!'), "red", ["bold"])
        exit(0)

values_input = ", ".join(str(i) for i in values_input_layer)
TAc.print(LANG.render_feedback("values_generated", f'The values for the input layer are: {values_input}'), "yellow", ["bold"])


# ====================== compute forward_propagation ==========================================
annl.compute_forward_propagation_with_print(instance, values_input_layer, ENV['activation'], ENV['watch_layers'],ENV['decimal_digits'], TAc, LANG)
