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
    ('activation',str)
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))


# START CODING YOUR SERVICE:

# get the instance
if ENV['instance_spec'] == 'catalogue1':
    format = 'plain.txt'
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
    # TODO insert regex for input provided by user
    instance_str = TALinput(str,TAc=TAc, LANG=LANG)
    instance = annl.get_instance_from_str(instance_str)
    '''
    instance_str = ''
    for token in instance_raw:
        instance_str += token
    '''

# generate the variables of the ANN
if ENV['instance_spec'] != 'random':
    TAc.print(LANG.render_feedback("instance", f'The instance on which the server will perform the forward propagation is:\n{" ".join(str(x) for x in instance[1])}, instance_id = {ENV["instance_id"]}'), "yellow", ["bold"]) 
else:
    TAc.print(LANG.render_feedback("instance", f'The instance on which the server will perform the forward propagation is:\n{" ".join(str(x) for x in instance[1])}, seed = {ENV["seed"]}'), "yellow", ["bold"]) 
n_nodes_input_layer = instance[1][0]
values_input_layer = [random.randint(-10,10) for _ in range(n_nodes_input_layer)] 
values_input = ", ".join(str(i) for i in values_input_layer)
TAc.print(LANG.render_feedback("values_generated", f'The values generated for the input layer are: {values_input}'), "yellow", ["bold"])

# compute forward_propagation
output = annl.compute_forward_propagation(instance, values_input_layer, ENV['activation'])
output = " ".join(str(round(x,2)) for x in output)
TAc.print(LANG.render_feedback("output", f'\nThe output is: {output}'), "white", ["bold"])
