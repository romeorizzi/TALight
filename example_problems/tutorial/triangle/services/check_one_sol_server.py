#!/usr/bin/env python3
from sys import stderr, exit
from triangle_lib import *
from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors
import random

# METADATA OF THIS TAL_SERVICE:
problem="triangle"
service="check_one_sol"
args_list = [
    ('n',int),
    ('MIN VAL',int),
    ('MAX VAL',int),
    ('how_to_input_the_triangle',str),
    ('sol_value',int),
    ('silent',int),
    ('lang',str),
]

ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 
n=ENV['n']
min_val = ENV['MIN VAL']
max_val = ENV['MAX VAL']
input_type = ENV['how_to_input_the_triangle']
sol_value = ENV['sol_value']
silent = ENV['silent']

# GENERAZIONE TRIANGOLO

if input_type == "lazy":
	undone = True
	while undone:
		values = input("Inserisci i valori del triangolo intervallati da uno spazio.")
		if len(values.split()) == sum(range(n+1)):
			triangle = values.split()
			undone = False
		else:
			print("Hai immesso " + str(len(values.split())) + " valori, riprova.")
else:
	triangle = random_triangle(n,int(input_type))
	
		
	
'''
def answer():
    if recognize(ENV["input_treatment"], TAc, LANG) and not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok", f'Your string is a feasible treatment with {len_input} pills.'), "yellow", ["bold"])
if n=='free':
    answer()
else:
    if len_input==int(n):
        answer()
    elif recognize(ENV["input_treatment"], TAc, LANG):
        TAc.print(LANG.render_feedback("different_lengths", f"No! Your string represents a feasible treatment but not of {n} pills."), "red", ["bold"])
'''
exit(0)
