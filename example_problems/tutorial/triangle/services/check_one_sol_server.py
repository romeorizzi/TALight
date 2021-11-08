#!/usr/bin/env python3
from sys import stderr, exit

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

import triangle_lib as tl

# METADATA OF THIS TAL_SERVICE:
problem="triangle"
service="check_one_sol"
args_list = [
    ('n',int),
    ('MIN_VAL',int),
    ('MAX_VAL',int),
    ('how_to_input_the_triangle',str),
    ('path',str),
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

if ENV['path'] == 'lazy':
	print(f"Insert the path as a sequence of L and R with no space in between.")
	path = input()
else:
	path = ENV['path']	
	
# CHECK WHETHER THE PATH CONTAINS ENOUGH DIRECTIONS

if len(path) != ENV['n']-1:
	TAc.print(LANG.render_feedback("wrong_directions_number", f"You inserted {len(path)} directions instead of the {ENV['n']-1} required. Remember not to insert spaces between the letters."), "red", ["bold"])
	exit(0)
elif any(x != "L" and x !="R" for x in path):
	TAc.print(LANG.render_feedback("wrong_direction",f"The path you inserted contains other directions than L or R."),"red", ["bold"])
	exit(0)
elif not ENV['silent']:
		if ENV['how_to_input_the_triangle'] == "lazy":
			TAc.print(LANG.render_feedback("right_triangle_and_directions_number", f"This solution is a feasible one for this problem.\nThe triangle you inserted is well formed and the path you chose consists of {ENV['n']-1} directions."), "green", ["bold"])
		else:
			TAc.print(LANG.render_feedback("right_directions_number", f"This solution is a feasible one for this problem.\nThe path you chose consists of {ENV['n']-1} directions."), "green", ["bold"])



exit(0)
