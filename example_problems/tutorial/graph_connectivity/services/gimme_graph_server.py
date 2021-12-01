#!/usr/bin/env python3
from sys import stderr, exit
from os import environ

from multilanguage import Env, Lang, TALcolors

import graph_connectivity_lib as gcl

# METADATA OF THIS TAL_SERVICE:
problem="graph_connectivity"
service="gimme_a_graph"
args_list = [
    ('n',int), 
    ('m',int), 
    ('graph_connectivity',str), 
    ('silent',bool),
#    ('display',str),
]

<<<<<<< HEAD
ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG = Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
=======
ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
>>>>>>> 06a1e8531187c650b1a93d5a6f5a63c10e00e24d

if environ["TAL_seed"] == "random_seed":
    # adjust the ENV['seed'] value to the solvability param
    if ENV['graph_connectivity'] == 'connected':
        ENV.arg['seed'] = gcl.gen_instance_seed(connected=True)
    elif ENV['graph_connectivity'] == 'disconnected':
        ENV.arg['seed'] = gcl.gen_instance_seed(connected=False)
            
g, graph_print, edges = gcl.generate_graph(ENV["n"], ENV["m"], ENV["seed"], TAc=TAc, LANG=LANG)

# Print Instance
if ENV['silent']:
<<<<<<< HEAD
    TAc.print(graph_print, "white", ["bold"])
=======
    print(graph_print)
>>>>>>> 06a1e8531187c650b1a93d5a6f5a63c10e00e24d
else:
    TAc.print(LANG.render_feedback("instance-descriptor", f'Here is the pseudo-random graph <n={ENV["n"]},m={ENV["m"]},seed={ENV["seed"]}>:'), "yellow", ["bold"])
    TAc.print(graph_print, "white", ["bold"])
    TAc.print(LANG.render_feedback("seed", f'The seed was: {ENV["seed"]}'), "yellow", ["bold"])

exit(0)
