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
    ('MIN_VAL',int),
    ('MAX_VAL',int),
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
min_val = ENV['MIN_VAL']
max_val = ENV['MAX_VAL']
input_type = ENV['how_to_input_the_triangle']
sol_value = ENV['sol_value']
silent = ENV['silent']

# GENERAZIONE TRIANGOLO

if input_type == "lazy":
	undone = True
	while undone:
		values = input("Inserisci i valori del triangolo intervallati da uno spazio.\n")
		if len(values.split(" ")) == sum(range(n+1)):
			triangle = values.split(" ")
			undone = False
		else:
			print("Hai immesso " + str(len(values.split(" "))) + " valori su " + str(sum(range(n+1))) + ", riprova.\n")
else:
	triangle = random_triangle(n,min_val,max_val,input_type)
	print(type(triangle))


# STAMPA TRIANGOLO

print("\nIl triangolo scelto è il seguente.\n")
print_triangle(n,triangle)
print("\n")

# INSERIMENTO PATH


undone = True
while undone:
	path_values = input("Inserisci la sequenza del percorso scelto utilizzando i valori L (left) o R (right) intervallati da uno spazio, escludendo il primo nodo.\n")
	if len(path_values.split(" ")) == n-1:
		path = path_values.split(" ")
		for direction in path:
			all_correct = True
			if direction != "R" and direction != "L":
				print("Hai inserito una direzione non valida, riprova.")
				break
			else:
				undone = False
	else:
		print("Hai immesso " + str(len(path_values.split(" "))) + " valori sui " + str(n-1) + " richiesti, riprova.\n")

for k in range(len(triangle)):
		triangle[k] = int(triangle[k])
		
# CALCOLO PATH
p,s = calculate_path(n,triangle,path)

print("Il path da te scelto è quello che tocca, nell\'ordine, i seguenti nodi: " + str(p))
print("Il costo totale del tuo path è :" + str(s))

			
	
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
