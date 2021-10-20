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
    ('sol_value',str),
    ('lang',str),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

# GENERAZIONE TRIANGOLO

if ENV['how_to_input_the_triangle'] == "lazy":
	undone = True
	while undone:
		values = input("Inserisci i valori del triangolo intervallati da uno spazio.\n")
		if len(values.split()) == sum(range(ENV['n']+1)):
			triangle = values.split()
			undone = False
		else:
			print("Hai immesso {str(len(values.split()))} valori su {str(sum(range(ENV['n']+1)))} riprova.\n")
else:
	triangle = random_triangle(ENV['n'],ENV['MIN_VAL'],ENV['MAX_VAL'],ENV['how_to_input_the_triangle'])


# STAMPA TRIANGOLO

print("\nIl triangolo scelto è il seguente.\n")
print_triangle(triangle)
print("\n")

# INSERIMENTO PATH


undone = True
while undone:
	path_values = input("Inserisci la sequenza del percorso scelto utilizzando i valori L (left) o R (right) intervallati da uno spazio, escludendo il primo nodo.\n\n")
	if len(path_values.split()) == n-1:
		path = path_values.split()
		if any((x != "R" and x != "L") for x in path):
			print("\nHai inserito una direzione non valida, riprova.\n")
		else:
			undone = False
	else:
		print("Hai immesso " + str(len(path_values.split())) + " valori sui " + str(ENV['n']-1) + " richiesti, riprova.\n")

for k in range(len(triangle)):
		triangle[k] = int(triangle[k])
		
# CALCOLO PATH
p,s = calculate_path(ENV['n'],triangle,path)

print("\nIl path da te scelto è quello che tocca, nell\'ordine, i seguenti nodi: " + str(p) + "\n")
print("Il costo totale del tuo path è: " + str(s))

			
	
'''
def answer():
    if recognize(ENV["input_treatment"], TAc, LANG) and not ENV["silent"]:
        TAc.OK()
        TAc.print(LANG.render_feedback("ok", f'Your string is a feasible treatment with {len_input} pills.'), "yellow", ["bold"])
if n=='free':
    answer()
else:
    if len_input==int(ENV['n']):
        answer()
    elif recognize(ENV["input_treatment"], TAc, LANG):
        TAc.print(LANG.render_feedback("different_lengths", f"No! Your string represents a feasible treatment but not of {n} pills."), "red", ["bold"])
'''
exit(0)
