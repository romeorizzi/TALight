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
    ('n_nodes',str),
    ('seed',int),
    ('instance_id',int),
    ('input_values',str),
    ('output_values',str),
    ('decimal_digits', int),
    ('activation',str)
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
    if ENV['seed'] == 'random_seed':
        TAc.print(LANG.render_feedback("random_seed_error", 'You are asking the check a solution on a new random instance, please insert the seed you get for the pseudo random generation'), "yellow", ["bold"])
        exit(0)

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


input_values = ENV['input_values'].split(' ')
input_values = list(map(float, input_values))

output_values = ENV['output_values'].split(' ')
output_values = list(map(float, output_values))
output_values = [round(num,ENV['decimal_digits']) for num in output_values]

# ====================== generate server solution ==========================================
server_output = annl.compute_forward_propagation(instance, input_values, ENV['activation'])
server_output = [round(num,ENV['decimal_digits']) for num in server_output]


#print(output_values, server_output)
if output_values == server_output:
    TAc.print(LANG.render_feedback("correct", f'Your output is correct!'), "green", ["bold"])
else:
    TAc.print(LANG.render_feedback("incorrect", f'No! Your output is not correct...'), "red", ["bold"])

exit(0)
