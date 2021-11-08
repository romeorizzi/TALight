#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
problem="triangle"
service="check_sol_value"
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('how_to_input_the_triangle',str),
    ('sol_value',str),
    ('silent',bool),
]


ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))
    
# START CODING YOUR SERVICE: 

# TRIANGLE GENERATION

if ENV['how_to_input_the_triangle'] == "lazy":
	triangle = []
	for i in range(1,ENV['n']+1):
		line = input(f"Insert the values of your triangle's line {i}.\n")
		line = line.split()
		line = [int(x) for x in line]
		if len(line) == i:
			triangle.append(line)
		else:
			TAc.print(LANG.render_feedback("wrong_elements_number", f"You inserted {len(line)} elements for line {i} instead of the {i} required."), "red", ["bold"])
			exit(0)
	if not ENV['silent']:
		TAc.print(LANG.render_feedback("right_triangle_insertion", f"Insertion completed."), "yellow", ["bold"])
else:
	triangle = tl.random_triangle(ENV['n'],ENV['MIN_VAL'],ENV['MAX_VAL'],ENV['how_to_input_the_triangle'])

# PRINT TRIANGLE
if not ENV['silent']:
	TAc.print(LANG.render_feedback("triangle_print", f"The triangle you chose is displayed here.\n\n"), "yellow", ["bold"])
	tl.print_triangle(triangle)

# GET PATH

if ENV['sol_value'] == 'lazy':
	print(f"Insert the path as a sequence of L and R with no spaces in between.")
	path = input()
	type_sol_value = 0	#--> sol_value is a path
elif ("R" in ENV['sol_value']) or ("L" in ENV['sol_value']):
	path = ENV['sol_value']	
	type_sol_value = 0	#--> sol_value is a path
else:
	s = int(ENV['sol_value'])
	type_sol_value = 1 #--> sol_value is a number



if type_sol_value == 0:
	# CHECK WHETHER THE PATH CONTAINS ENOUGH DIRECTIONS
	
	if len(path) != ENV['n']-1:
		TAc.print(LANG.render_feedback("wrong_directions_number", f"You inserted {len(path)} directions instead of the {ENV['n']-1} required. Remember not to insert spaces between the letters."), "red", ["bold"])
		exit(0)
	elif any(x != "L" and x !="R" for x in path):
		TAc.print(LANG.render_feedback("wrong_direction",f"The path you inserted contains other directions than L or R."),"red", ["bold"])
		exit(0)
	if not ENV['silent']:
		TAc.print(LANG.render_feedback("path_print",f"The path you inserted is displayed here.\n\n"),"yellow", ["bold"])
		print_path(triangle,path)
	# CALCULATE PATH
	
	_,s = calculate_path(triangle,path)

best = best_path_cost(triangle)

if type_sol_value == 1:
	if not ENV['silent']:
		if int(ENV['sol_value']) == best:	
			TAc.print(LANG.render_feedback("right_best_sol_value",f"\nWe agree. The value you entered is the best solution for your triangle."),"green", ["bold"])			
	if int(ENV['sol_value']) != best:	
		TAc.print(LANG.render_feedback("wrong_best_sol_value",f"\nWe don't agree, the value you entered is not the best solution for your triangle."),"red", ["bold"])
else:
	if not ENV['silent']:
		if s == best:	
			TAc.print(LANG.render_feedback("right_best_path",f"\nWe agree. The path you chose has the best cost for your triangle."),"green", ["bold"])			
	if s != best:	
		TAc.print(LANG.render_feedback("wrong_best_path",f"\nWe don't agree, the path you chose has not the best cost for your triangle."),"red", ["bold"])

exit(0)
