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
    ('path',str),
    ('silent',bool),
    ('lang',str),
]


ENV =Env(problem, service, args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

# GENERAZIONE TRIANGOLO

if ENV['how_to_input_the_triangle'] == "lazy":
	triangle = []
	for i in range(1,ENV['n']+1):
		line = input(f"Inserisci i valori della riga {i} del tuo triangolo.\n")
		line = line.split()
		line = [int(x) for x in line]
		if len(line) == i:
			triangle.append(line)
		else:
			TAc.print(LANG.render_feedback("wrong_elements_number", f"Nella riga {i} hai inserito {len(line)} elementi anziché {i}."), "red", ["bold"])
			exit(0)
	if not ENV['silent']:
		TAc.print(LANG.render_feedback("right_triangle_insertion", f"Inserimento del triangolo riuscito"), "yellow", ["bold"])
else:
	triangle = random_triangle(ENV['n'],ENV['MIN_VAL'],ENV['MAX_VAL'],ENV['how_to_input_the_triangle'])


# STAMPA TRIANGOLO

print_triangle(triangle)


# INSERIMENTO PATH

if len(ENV['path']) != ENV['n']-1:
	TAc.print(LANG.render_feedback("wrong_directions_number", f"Hai inserito {len(ENV['path'])} direzioni rispetto alle {ENV['n']-1} richieste."), "red", ["bold"])
	exit(0)
elif not ENV['silent']:
		TAc.print(LANG.render_feedback("right_directions_number", f"Esatto. Hai inserito {len(ENV['path'])} direzioni sulle {ENV['n']-1} richieste."), "yellow", ["bold"])


		
# CALCOLO PATH
p,s = calculate_path(triangle,ENV['path'])

if not ENV['silent']:
	TAc.print(LANG.render_feedback("show_path",f"Il path da te scelto è quello che tocca, nell\'ordine, i seguenti nodi: {p}"),"yellow", ["bold"])

if ENV['sol_value'] !=	"not_relevant":
	if int(ENV['sol_value']) == s:	
		TAc.print(LANG.render_feedback("right_sol_value",f"Ti confermiamo che il path da te scelto ha costo {s}."),"green", ["bold"])			
	else:
		TAc.print(LANG.render_feedback("wrong_sol_value",f"Attenzione, il path da te scelto non ha costo {ENV['sol_value']}."),"red", ["bold"])
		if not ENV['silent']:
			TAc.print(LANG.render_feedback("correct_path_value",f"Il path da te scelto in realtà ha costo {s}."),"yellow", ["bold"])
exit(0)
